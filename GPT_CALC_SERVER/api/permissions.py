from rest_framework.permissions import BasePermission

class IsDeviceAuthenticated(BasePermission):
    message = "You must be an authenticated device to access this endpoint."

    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, "id"))
