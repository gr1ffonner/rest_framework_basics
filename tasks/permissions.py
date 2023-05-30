from rest_framework import permissions

UNSAFE_METHODS = ["POST", "DELETE", "PUT"]


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in UNSAFE_METHODS and request.user.role == "manager":
            return True
        else:
            return False
