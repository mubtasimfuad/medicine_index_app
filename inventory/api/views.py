import logging
from rest_framework.views import APIView
from rest_framework import status
from authentication.permissions import IsAdminOrReadOnly
from inventory.utils import api_response
from .serializers import MedicineDetailSerializer
from ..models import MedicineDetail
from ..exceptions import FeaturedMedicineInvalidError, NotFoundError
from utils.redis_cache import RedisCache

# Cache keys and lock definitions
cache_manager = RedisCache()
MEDICINE_LIST_CACHE_KEY = "medicine_list"
MEDICINE_DETAIL_CACHE_KEY_TEMPLATE = "medicine_detail_{}"
MEDICINE_LIST_LOCK_KEY = "medicine_list_lock"
app_logger = logging.getLogger("app_logger")
error_logger = logging.getLogger("error_logger")


class MedicineListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """Retrieve a list of medicines."""
        try:
            app_logger.info("Attempting to retrieve cached medicine list")
            cached_data = cache_manager.get(MEDICINE_LIST_CACHE_KEY)
            if cached_data:
                app_logger.info("Cache hit for medicine list")
                return api_response(success=True, data=cached_data)

            # Cache miss - retrieve from DB
            app_logger.info("Cache miss for medicine list. Querying database.")
            medicines = MedicineDetail.objects.all()
            data = MedicineDetailSerializer(medicines, many=True).data
            cache_manager.set(MEDICINE_LIST_CACHE_KEY, data, expiration=900)
            return api_response(success=True, data=data)

        except Exception as e:
            error_logger.error("Error in MedicineListView GET method: %s", str(e))
            return api_response(
                success=False,
                message="An error occurred while retrieving medicines.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """Create a new medicine entry and invalidate list cache."""
        app_logger.info("POST request received to create a new medicine entry")
        lock = cache_manager.acquire_lock(MEDICINE_LIST_LOCK_KEY)
        if not lock:
            error_logger.warning("Failed to acquire lock for POST /api/medicines/")
            return api_response(
                success=False,
                message="Service is busy. Please try again.",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            serializer = MedicineDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache_manager.delete(MEDICINE_LIST_CACHE_KEY)
                app_logger.info("Created new medicine and invalidated list cache.")
                return api_response(
                    success=True,
                    data=serializer.data,
                    message="Medicine created successfully.",
                    status_code=status.HTTP_201_CREATED,
                )
            error_logger.error("Validation failed for POST: %s", serializer.errors)
            return api_response(
                success=False,
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except FeaturedMedicineInvalidError as e:
            error_logger.error("Custom validation error: %s", str(e))
            return api_response(
                success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            error_logger.error("Exception in MedicineListView POST method: %s", str(e))
            return api_response(
                success=False,
                message="An error occurred while creating the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            cache_manager.release_lock(lock)


class MedicineDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        """Retrieve a single medicine entry."""
        cache_key = MEDICINE_DETAIL_CACHE_KEY_TEMPLATE.format(pk)
        try:
            app_logger.info(f"Fetching medicine entry with ID: {pk}")
            cached_data = cache_manager.get(cache_key)
            if cached_data:
                app_logger.info(f"Cache hit for medicine ID {pk}")
                return api_response(success=True, data=cached_data)

            # Cache miss - retrieve from DB
            medicine = MedicineDetail.objects.get(pk=pk)
            data = MedicineDetailSerializer(medicine).data
            cache_manager.set(cache_key, data, expiration=900)
            return api_response(success=True, data=data)

        except MedicineDetail.DoesNotExist:
            error_logger.error(f"Medicine with ID {pk} not found.")
            return api_response(
                success=False,
                message="Medicine not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            error_logger.error(f"Error in MedicineDetailView GET method: {str(e)}")
            return api_response(
                success=False,
                message="An error occurred while retrieving the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        """Update a specific medicine entry."""
        lock_key = MEDICINE_LIST_LOCK_KEY
        cache_key = MEDICINE_DETAIL_CACHE_KEY_TEMPLATE.format(pk)
        lock = cache_manager.acquire_lock(lock_key)
        if not lock:
            return api_response(
                success=False,
                message="Service is busy. Please try again.",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            medicine = MedicineDetail.objects.get(pk=pk)
            serializer = MedicineDetailSerializer(
                medicine, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                cache_manager.delete(cache_key)
                cache_manager.delete(MEDICINE_LIST_CACHE_KEY)
                return api_response(
                    success=True,
                    data=serializer.data,
                    message="Medicine updated successfully.",
                    status_code=status.HTTP_200_OK,
                )
            return api_response(
                success=False,
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except MedicineDetail.DoesNotExist:
            return api_response(
                success=False,
                message="Medicine not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        finally:
            cache_manager.release_lock(lock)

    def delete(self, request, pk):
        """Delete a specific medicine entry."""
        lock = cache_manager.acquire_lock(MEDICINE_LIST_LOCK_KEY)
        cache_key = MEDICINE_DETAIL_CACHE_KEY_TEMPLATE.format(pk)
        if not lock:
            return api_response(
                success=False,
                message="Service is busy. Please try again.",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            medicine = MedicineDetail.objects.get(pk=pk)
            medicine.delete()
            cache_manager.delete(cache_key)
            cache_manager.delete(MEDICINE_LIST_CACHE_KEY)
            return api_response(
                success=True,
                message="Medicine deleted successfully.",
                status_code=status.HTTP_204_NO_CONTENT,
            )

        except MedicineDetail.DoesNotExist:
            error_logger.error("Medicine not found for deletion: ID %s", pk)
            return api_response(
                success=False,
                message="Medicine not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            error_logger.error(f"Exception in DELETE method: {str(e)}")
            return api_response(
                success=False,
                message="An error occurred while deleting the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            cache_manager.release_lock(lock)
