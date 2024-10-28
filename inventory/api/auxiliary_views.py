#inventory/api/auxiliary_views.py
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


class GenericNameListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        generic_names = GenericName.objects.all()
        serializer = GenericNameSerializer(generic_names, many=True)
        return api_response(success=True, data=serializer.data)

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

    def get(self, request):
        categories = MedicineCategory.objects.all()
        serializer = MedicineCategorySerializer(categories, many=True)
        return api_response(success=True, data=serializer.data)

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

    def get(self, request):
        forms = MedicineForm.objects.all()
        serializer = MedicineFormSerializer(forms, many=True)
        return api_response(success=True, data=serializer.data)

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

    def get(self, request):
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)
        return api_response(success=True, data=serializer.data)

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
