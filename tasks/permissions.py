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


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS requests for all authenticated users
        elif request.user.is_authenticated:
            return (
                request.user.role == "employee"
            )  # Only users with role "employee" can perform unsafe methods
        else:
            return False  # Deny all other requests

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS requests for all authenticated users
        elif request.user.is_authenticated and request.user.role == "employee":
            return (
                obj.assigned_to == request.user
            )  # Only the assigned employee can modify the task
        else:
            return False  # Deny all other requests
