from rest_framework.permissions import BasePermission

class IsRoleAdmin(BasePermission):
    """
    Allows access only to users with role = 1
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user.role, "name", None) == "Admin"
        )
    

class IsRoleUser(BasePermission):
    """
    Allows access only to users with role = 2
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user.role, "name", None) == "User"
        )