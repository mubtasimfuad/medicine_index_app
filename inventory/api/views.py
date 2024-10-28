# inventory/views.py

import json
import logging
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from authentication.permissions import IsAdminOrReadOnly
from inventory.exceptions import FeaturedMedicineInvalidError
from inventory.utils import api_response
from .serializers import MedicineDetailSerializer
from ..models import MedicineDetail
from utils.redis_cache import RedisCache

# Redis cache manager
cache_manager = RedisCache()
# Define cache keys and other constants
MEDICINE_LIST_CACHE_KEY = "medicine_list"
MEDICINE_DETAIL_CACHE_KEY_TEMPLATE = "medicine_detail_{}"
SEARCH_CACHE_KEY_TEMPLATE = "medicine_search_{}"

app_logger = logging.getLogger("app_logger")
error_logger = logging.getLogger("error_logger")


class MedicineListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all medicines, with data caching enabled for faster retrieval on subsequent requests.",
        responses={
            200: openapi.Response(
                description="A list of medicines",
                schema=MedicineDetailSerializer(many=True),
            ),
            500: "Internal Server Error - Error occurred while retrieving medicines.",
        },
    )
    def get(self, request):
        """Retrieve a list of medicines with caching."""
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

    @swagger_auto_schema(
        operation_description="Create a new medicine entry with provided details. Only accessible to users with appropriate permissions.",
        request_body=MedicineDetailSerializer,
        responses={
            201: openapi.Response(
                description="Medicine created successfully",
                schema=MedicineDetailSerializer,
            ),
            400: "Bad Request - Validation error in the provided data.",
            500: "Internal Server Error - Error occurred while creating the medicine.",
        },
    )
    def post(self, request):
        """Create a new medicine entry."""
        app_logger.info("POST request received to create a new medicine entry")
        try:
            serializer = MedicineDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                app_logger.info("Created new medicine entry.")
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


class MedicineDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a specific medicine entry by its ID, with caching enabled for faster subsequent retrieval.",
        responses={
            200: openapi.Response(
                description="Details of the requested medicine",
                schema=MedicineDetailSerializer,
            ),
            404: "Not Found - Medicine with the given ID does not exist.",
            500: "Internal Server Error - Error occurred while retrieving the medicine.",
        },
    )
    def get(self, request, pk):
        """Retrieve a single medicine entry with caching."""
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

    @swagger_auto_schema(
        operation_description="Update a specific medicine entry by its ID. Only accessible to users with appropriate permissions.",
        request_body=MedicineDetailSerializer,
        responses={
            200: openapi.Response(
                description="Medicine updated successfully",
                schema=MedicineDetailSerializer,
            ),
            400: "Bad Request - Validation error in the provided data.",
            404: "Not Found - Medicine with the given ID does not exist.",
            500: "Internal Server Error - Error occurred while updating the medicine.",
        },
    )
    def put(self, request, pk):
        """Update a specific medicine entry."""
        try:
            medicine = MedicineDetail.objects.get(pk=pk)
            serializer = MedicineDetailSerializer(
                medicine, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
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

    @swagger_auto_schema(
        operation_description="Delete a specific medicine entry by its ID. Only accessible to users with appropriate permissions.",
        responses={
            204: "No Content - Medicine deleted successfully.",
            404: "Not Found - Medicine with the given ID does not exist.",
            500: "Internal Server Error - Error occurred while deleting the medicine.",
        },
    )
    def delete(self, request, pk):
        """Delete a specific medicine entry."""
        try:
            medicine = MedicineDetail.objects.get(pk=pk)
            medicine.delete()
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


class MedicineSearchView(APIView):
    """
    A view to perform a full-text search on medicines with caching, including highlighting metadata with start and end indices.
    """

    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Search for medicines by name, generic name, or using specific filters. "
        "Accessible to users with appropriate permissions.",
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Search query string",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "filters",
                openapi.IN_QUERY,
                description="Additional filters in JSON format",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Search results with highlight positions",
                schema=MedicineDetailSerializer(many=True),
            ),
            400: "Bad Request - Query parameter 'q' is required.",
            403: "Forbidden - You do not have permission to access this resource.",
            500: "Internal Server Error",
        },
    )
    def get(self, request):
        """Perform a full-text search on medicines with caching and highlight metadata."""
        query = request.query_params.get("q", "").strip()
        filters = request.query_params.get("filters", "")
        cache_key = SEARCH_CACHE_KEY_TEMPLATE.format(query)

        # Validate required search parameter
        if not query:
            return api_response(
                success=False,
                message="Query parameter 'q' is required for search.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Try to retrieve cached results
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            app_logger.info(f"Cache hit for search query: '{query}'")
            return api_response(success=True, data=cached_data)

        # Proceed with database search if cache miss
        app_logger.info(f"Cache miss for search query: '{query}' - querying database")
        try:
            search_filter = Q(name__icontains=query) | Q(
                generic_name__name__icontains=query
            )

            # Apply additional filters, if any
            if filters:
                try:
                    filter_params = json.loads(filters)
                    for key, value in filter_params.items():
                        search_filter &= Q(**{key: value})
                except json.JSONDecodeError:
                    error_logger.error(f"Invalid JSON format for filters: {filters}")
                    return api_response(
                        success=False,
                        message="Filters must be a valid JSON string.",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

            # Perform the search and serialize the results
            medicines = MedicineDetail.objects.filter(search_filter).distinct()
            results = []
            for medicine in medicines:
                serialized_data = MedicineDetailSerializer(medicine).data
                matches = {
                    "name": self.get_match_indices_with_end(medicine.name, query),
                    "generic_name": (
                        self.get_match_indices_with_end(
                            medicine.generic_name.name, query
                        )
                        if medicine.generic_name
                        else []
                    ),
                }
                # Append the matches metadata to each result
                serialized_data["matches"] = matches
                results.append(serialized_data)

            # Cache the search results with highlight metadata
            cache_manager.set(
                cache_key, results, expiration=600
            )  # Cache for 10 minutes
            return api_response(success=True, data=results)

        except Exception as e:
            error_logger.error(f"Error in MedicineSearchView GET method: {str(e)}")
            return api_response(
                success=False,
                message="An error occurred while searching for medicines.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_match_indices_with_end(self, text, query):
        """
        Helper method to find start and end indices of `query` in `text`.
        """
        matches = []
        query = query.lower()
        text = text.lower()
        start = 0
        while start < len(text):
            start = text.find(query, start)
            if start == -1:
                break
            end = start + len(query)
            matches.append((start, end))
            start = end
        return matches
