# inventory/views.py

import json
import logging
from rest_framework.views import APIView
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from authentication.permissions import IsAdminOrReadOnly
from inventory.exceptions import FeaturedMedicineInvalidError
from inventory.utils import api_response
from .serializers import MedicineDetailSerializer
from ..models import MedicineDetail
from utils.redis_cache import RedisCache
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# Redis cache manager
cache_manager = RedisCache()
# Define cache keys and other constants
MEDICINE_LIST_CACHE_KEY = "medicine_list"
MEDICINE_DETAIL_CACHE_KEY_TEMPLATE = "medicine_detail_{}"
SEARCH_CACHE_KEY_TEMPLATE = "medicine_search_{}"

app_logger = logging.getLogger("app_logger")
error_logger = logging.getLogger("error_logger")


class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = "page_size"
    max_page_size = 100


class MedicineListView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsPagination

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of all medicines with optional caching.",
        responses={
            200: openapi.Response(
                description="A paginated list of medicines",
                schema=MedicineDetailSerializer(many=True),
            ),
            500: "Internal Server Error - Error occurred while retrieving medicines.",
        },
    )
    def get(self, request):
        """Retrieve a paginated list of medicines with optional caching."""
        try:
            app_logger.info("Attempting to retrieve paginated medicine list")
            page = request.query_params.get("page", 1)
            cache_key = f"{MEDICINE_LIST_CACHE_KEY}_page_{page}"

            # Check for cached data
            # cached_data = cache_manager.get(cache_key)
            # if cached_data:
            #     app_logger.info("Cache hit for paginated medicine list")
            #     return api_response(success=True, data=cached_data)

            # Retrieve and paginate data
            medicines = (
                MedicineDetail.objects.select_related(
                    "generic_name", "category", "form", "manufacturer"
                )
                .prefetch_related("conditions")
                .all()
            )
            paginator = StandardResultsPagination()
            result_page = paginator.paginate_queryset(medicines, request)
            serialized_data = MedicineDetailSerializer(result_page, many=True).data

            # Cache the paginated results
            cache_manager.set(cache_key, serialized_data, expiration=900)
            return paginator.get_paginated_response(serialized_data)

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
        except Exception as e:
            error_logger.error(f"Exception in MedicineDetailView PUT method: {str(e)}")
            return api_response(
                success=False,
                message="An error occurred while updating the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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


from rest_framework.response import Response
from inventory.models import MedicineCategory, MedicineForm, Manufacturer


class MedicineSearchView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """Perform a paginated search with caching and keyword highlighting."""
        try:
            app_logger.info("GET request received for MedicineSearchView")
            query = request.query_params.get("q", "").strip()
            filters = request.query_params.get("filters", "")
            page = request.query_params.get("page", 1)
            cache_key = f"{SEARCH_CACHE_KEY_TEMPLATE.format(query)}_page_{page}"

            if not query:
                return api_response(
                    success=False,
                    message="Query parameter 'q' is required for search.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Check for cached response
            cached_data = cache_manager.get(cache_key)
            if cached_data:
                app_logger.info(f"Cache hit for search query '{query}' on page {page}")
                return Response(cached_data)

            # Construct filters using ID mappings
            search_filter = Q(name__icontains=query) | Q(
                generic_name__name__icontains=query
            )
            if filters:
                filter_params = json.loads(filters)
                search_filter = self.build_search_filter(search_filter, filter_params)

            # Retrieve and paginate the results
            medicines = MedicineDetail.objects.filter(search_filter).distinct()
            paginator = StandardResultsPagination()
            result_page = paginator.paginate_queryset(medicines, request)

            # No results handling
            if not result_page:
                empty_response = paginator.get_paginated_response([])
                cache_manager.set(cache_key, empty_response.data, expiration=600)
                return empty_response

            # Serialize and cache results
            results = [
                self._add_highlighting(MedicineDetailSerializer(med).data, query)
                for med in result_page
            ]
            paginated_response = paginator.get_paginated_response(results)
            cache_manager.set(cache_key, paginated_response.data, expiration=600)
            return paginated_response

        except Exception as e:
            error_logger.error(f"Error in MedicineSearchView GET method: {str(e)}")
            return api_response(
                success=False,
                message="An error occurred while searching for medicines.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def build_search_filter(self, search_filter, filter_params):
        """Helper to build a search filter from filter parameters."""
        try:
            if "category" in filter_params and filter_params["category"]:
                category_id = MedicineCategory.objects.get(
                    id=filter_params["category"]
                ).id
                search_filter &= Q(category_id=category_id)

            if "form" in filter_params and filter_params["form"]:
                form_id = MedicineForm.objects.get(id=filter_params["form"]).id
                search_filter &= Q(form_id=form_id)

            if "manufacturer" in filter_params and filter_params["manufacturer"]:
                manufacturer_id = Manufacturer.objects.get(
                    id=filter_params["manufacturer"]
                ).id
                search_filter &= Q(manufacturer_id=manufacturer_id)

        except MedicineCategory.DoesNotExist:
            error_logger.error("Invalid category filter")
        except MedicineForm.DoesNotExist:
            error_logger.error("Invalid form filter")
        except Manufacturer.DoesNotExist:
            error_logger.error("Invalid manufacturer filter")

        return search_filter

    def _add_highlighting(self, data, query):
        """Adds highlight positions to data."""
        matches = {
            "name": self.get_match_indices_with_end(data["name"], query),
            "generic_name": (
                self.get_match_indices_with_end(
                    data["generic_name_details"]["name"], query
                )
                if "generic_name_details" in data and data["generic_name_details"]
                else []
            ),
        }
        data["matches"] = matches
        return data

    def get_match_indices_with_end(self, text, query):
        """Helper to find start and end indices of `query` in `text`."""
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
