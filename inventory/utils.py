from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from .exceptions import FeaturedMedicineInvalidError, NotFoundError, ValidationError


def custom_exception_handler(exc, context):
    """Custom exception handler to return standardized API responses for errors."""
    if isinstance(exc, (FeaturedMedicineInvalidError, NotFoundError, ValidationError)):
        return (
            exc.get_full_details()
        )  # Custom exceptions with specific status codes and details
    response = exception_handler(exc, context)
    if response is not None:
        return api_response(
            success=False, message=response.data, status_code=response.status_code
        )
    return api_response(
        success=False, message="An unexpected error occurred.", status_code=500
    )


def api_response(success, data=None, message=None, status_code=status.HTTP_200_OK):
    """Universal response format for all API responses."""
    return Response(
        {"success": success, "data": data, "message": message}, status=status_code
    )
