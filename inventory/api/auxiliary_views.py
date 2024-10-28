# inventory/api/auxiliary_views.py
from rest_framework import status, permissions
from rest_framework.views import APIView

from ..models import GenericName, MedicineCategory, MedicineForm, Manufacturer
from .serializers import (
    GenericNameSerializer,
    MedicineCategorySerializer,
    MedicineFormSerializer,
    ManufacturerSerializer,
)
from ..utils import api_response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GenericNameListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all generic names.",
        responses={
            200: openapi.Response(
                description="List of generic names",
                schema=GenericNameSerializer(many=True),
            )
        },
    )
    def get(self, request):
        generic_names = GenericName.objects.all()
        serializer = GenericNameSerializer(generic_names, many=True)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new generic name.",
        request_body=GenericNameSerializer,
        responses={
            201: openapi.Response(
                description="Generic name created successfully",
                schema=GenericNameSerializer,
            ),
            400: "Bad Request - Validation errors",
        },
    )
    def post(self, request):
        serializer = GenericNameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Generic name created successfully.",
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class GenericNameRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return GenericName.objects.get(pk=pk)
        except GenericName.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a specific generic name by ID.",
        responses={
            200: openapi.Response(
                description="Generic name details",
                schema=GenericNameSerializer,
            ),
            404: "Not Found - Generic name not found",
        },
    )
    def get(self, request, pk):
        generic_name = self.get_object(pk)
        if not generic_name:
            return api_response(
                success=False,
                message="Generic name not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = GenericNameSerializer(generic_name)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific generic name by ID.",
        request_body=GenericNameSerializer,
        responses={
            200: openapi.Response(
                description="Generic name updated successfully",
                schema=GenericNameSerializer,
            ),
            400: "Bad Request - Validation errors",
            404: "Not Found - Generic name not found",
        },
    )
    def put(self, request, pk):
        generic_name = self.get_object(pk)
        if not generic_name:
            return api_response(
                success=False,
                message="Generic name not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = GenericNameSerializer(
            generic_name, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Generic name updated successfully.",
                status_code=status.HTTP_200_OK,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a specific generic name by ID.",
        responses={
            204: "No Content - Generic name deleted successfully",
            404: "Not Found - Generic name not found",
        },
    )
    def delete(self, request, pk):
        generic_name = self.get_object(pk)
        if not generic_name:
            return api_response(
                success=False,
                message="Generic name not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        generic_name.delete()
        return api_response(
            success=True,
            message="Generic name deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class MedicineCategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all medicine categories.",
        responses={
            200: openapi.Response(
                description="List of medicine categories",
                schema=MedicineCategorySerializer(many=True),
            )
        },
    )
    def get(self, request):
        categories = MedicineCategory.objects.all()
        serializer = MedicineCategorySerializer(categories, many=True)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new medicine category.",
        request_body=MedicineCategorySerializer,
        responses={
            201: openapi.Response(
                description="Medicine category created successfully",
                schema=MedicineCategorySerializer,
            ),
            400: "Bad Request - Validation errors",
        },
    )
    def post(self, request):
        serializer = MedicineCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Medicine category created successfully.",
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class MedicineCategoryRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return MedicineCategory.objects.get(pk=pk)
        except MedicineCategory.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a specific medicine category by ID.",
        responses={
            200: openapi.Response(
                description="Medicine category details",
                schema=MedicineCategorySerializer,
            ),
            404: "Not Found - Medicine category not found",
        },
    )
    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return api_response(
                success=False,
                message="Medicine category not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = MedicineCategorySerializer(category)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific medicine category by ID.",
        request_body=MedicineCategorySerializer,
        responses={
            200: openapi.Response(
                description="Medicine category updated successfully",
                schema=MedicineCategorySerializer,
            ),
            400: "Bad Request - Validation errors",
            404: "Not Found - Medicine category not found",
        },
    )
    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return api_response(
                success=False,
                message="Medicine category not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = MedicineCategorySerializer(
            category, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Medicine category updated successfully.",
                status_code=status.HTTP_200_OK,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a specific medicine category by ID.",
        responses={
            204: "No Content - Medicine category deleted successfully",
            404: "Not Found - Medicine category not found",
        },
    )
    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return api_response(
                success=False,
                message="Medicine category not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        category.delete()
        return api_response(
            success=True,
            message="Medicine category deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class MedicineFormListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all medicine forms.",
        responses={
            200: openapi.Response(
                description="List of medicine forms",
                schema=MedicineFormSerializer(many=True),
            )
        },
    )
    def get(self, request):
        forms = MedicineForm.objects.all()
        serializer = MedicineFormSerializer(forms, many=True)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new medicine form.",
        request_body=MedicineFormSerializer,
        responses={
            201: openapi.Response(
                description="Medicine form created successfully",
                schema=MedicineFormSerializer,
            ),
            400: "Bad Request - Validation errors",
        },
    )
    def post(self, request):
        serializer = MedicineFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Medicine form created successfully.",
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class MedicineFormRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return MedicineForm.objects.get(pk=pk)
        except MedicineForm.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a specific medicine form by ID.",
        responses={
            200: openapi.Response(
                description="Medicine form details",
                schema=MedicineFormSerializer,
            ),
            404: "Not Found - Medicine form not found",
        },
    )
    def get(self, request, pk):
        form = self.get_object(pk)
        if not form:
            return api_response(
                success=False,
                message="Medicine form not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = MedicineFormSerializer(form)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific medicine form by ID.",
        request_body=MedicineFormSerializer,
        responses={
            200: openapi.Response(
                description="Medicine form updated successfully",
                schema=MedicineFormSerializer,
            ),
            400: "Bad Request - Validation errors",
            404: "Not Found - Medicine form not found",
        },
    )
    def put(self, request, pk):
        form = self.get_object(pk)
        if not form:
            return api_response(
                success=False,
                message="Medicine form not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = MedicineFormSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Medicine form updated successfully.",
                status_code=status.HTTP_200_OK,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a specific medicine form by ID.",
        responses={
            204: "No Content - Medicine form deleted successfully",
            404: "Not Found - Medicine form not found",
        },
    )
    def delete(self, request, pk):
        form = self.get_object(pk)
        if not form:
            return api_response(
                success=False,
                message="Medicine form not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        form.delete()
        return api_response(
            success=True,
            message="Medicine form deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class ManufacturerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all manufacturers.",
        responses={
            200: openapi.Response(
                description="List of manufacturers",
                schema=ManufacturerSerializer(many=True),
            )
        },
    )
    def get(self, request):
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)
        return api_response(success=True, data=serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new manufacturer.",
        request_body=ManufacturerSerializer,
        responses={
            201: openapi.Response(
                description="Manufacturer created successfully",
                schema=ManufacturerSerializer,
            ),
            400: "Bad Request - Validation errors",
        },
    )
    def post(self, request):
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Manufacturer created successfully.",
                status_code=status.HTTP_201_CREATED,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class ManufacturerRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Manufacturer.objects.get(pk=pk)
        except Manufacturer.DoesNotExist:
            return None
    @swagger_auto_schema(
        operation_description="Retrieve a specific manufacturer by ID.",
        responses={
            200: openapi.Response(
                description="Manufacturer details",
                schema=ManufacturerSerializer,
            ),
            404: "Not Found - Manufacturer not found",
        }
    )

    def get(self, request, pk):
        manufacturer = self.get_object(pk)
        if not manufacturer:
            return api_response(
                success=False,
                message="Manufacturer not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = ManufacturerSerializer(manufacturer)
        return api_response(success=True, data=serializer.data)
    @swagger_auto_schema(
        operation_description="Update a specific manufacturer by ID.",
        request_body=ManufacturerSerializer,
        responses={
            200: openapi.Response(
                description="Manufacturer updated successfully",
                schema=ManufacturerSerializer,
            ),
            400: "Bad Request - Validation errors",
            404: "Not Found - Manufacturer not found",
        }
    )

    def put(self, request, pk):
        manufacturer = self.get_object(pk)
        if not manufacturer:
            return api_response(
                success=False,
                message="Manufacturer not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = ManufacturerSerializer(
            manufacturer, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                success=True,
                data=serializer.data,
                message="Manufacturer updated successfully.",
                status_code=status.HTTP_200_OK,
            )
        return api_response(
            success=False,
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    @swagger_auto_schema(
        operation_description="Delete a specific manufacturer by ID.",
        responses={
            204: "No Content - Manufacturer deleted successfully",
            404: "Not Found - Manufacturer not found",
        }
    )

    def delete(self, request, pk):
        manufacturer = self.get_object(pk)
        if not manufacturer:
            return api_response(
                success=False,
                message="Manufacturer not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        manufacturer.delete()
        return api_response(
            success=True,
            message="Manufacturer deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )
