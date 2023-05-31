from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS requests for all authenticated users
        elif request.user.is_authenticated:
            return (
                request.user.role == "manager"
            )  # Only users with role "manager" can perform unsafe methods
        else:
            return False  # Deny all other requests
