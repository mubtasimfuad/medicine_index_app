from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admins to create, update, or delete medicines.
    Public users can only view (GET requests).
    """

    def has_permission(self, request, view):
        # SAFE_METHODS include GET, HEAD, and OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        # Only admin users can perform unsafe methods like POST, PUT, DELETE.
        return request.user and request.user.is_authenticated and request.user.is_staff
