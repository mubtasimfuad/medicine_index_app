# inventory/exceptions.py

from rest_framework import status
from rest_framework.exceptions import APIException


class FeaturedMedicineInvalidError(APIException):
    """Raised when there is an attempt to mark multiple medicines as featured for a single generic."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Only one featured medicine is allowed per generic name."
    default_code = "featured_medicine_invalid"


class NotFoundError(APIException):
    """Raised when a requested resource is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The requested resource was not found."
    default_code = "not_found"


class ValidationError(APIException):
    """Raised when data validation fails."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Validation error."
    default_code = "validation_error"
