# inventory/api/views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import MedicineDetailSerializer
from ..models import MedicineDetail
from ..exceptions import FeaturedMedicineInvalidError, NotFoundError, ValidationError
from ..utils import api_response


class MedicineDetailView(APIView):
    def get(self, request, pk=None):
        """Retrieve a single or list of medicines."""
        try:
            if pk:
                try:
                    medicine = MedicineDetail.objects.get(pk=pk)
                    serializer = MedicineDetailSerializer(medicine)
                    return api_response(success=True, data=serializer.data)
                except MedicineDetail.DoesNotExist:
                    raise NotFoundError("Medicine not found.")
            else:
                medicines = MedicineDetail.objects.all()
                serializer = MedicineDetailSerializer(medicines, many=True)
                return api_response(success=True, data=serializer.data)

        except NotFoundError as e:
            return api_response(
                success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return api_response(
                success=False,
                message="An error occurred while retrieving medicines.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            serializer = MedicineDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return api_response(
                    success=True,
                    data=serializer.data,
                    message="Medicine created successfully.",
                    status_code=status.HTTP_201_CREATED,
                )
            else:
                return api_response(
                    success=False,
                    message=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        except FeaturedMedicineInvalidError as e:
            return Response(
                {"success": False, "data": None, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return api_response(
                success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return api_response(
                success=False,
                message="An error occurred while creating the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        """Update a medicine entry."""
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
        except FeaturedMedicineInvalidError as e:
            return api_response(
                success=False,
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return api_response(
                success=False,
                message="An error occurred while updating the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, pk):
        """Delete a medicine entry."""
        try:
            medicine = MedicineDetail.objects.get(pk=pk)
            medicine.delete()
            return api_response(
                success=True,
                message="Medicine deleted successfully.",
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except MedicineDetail.DoesNotExist:
            return api_response(
                success=False,
                message="Medicine not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return api_response(
                success=False,
                message="An error occurred while deleting the medicine.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
