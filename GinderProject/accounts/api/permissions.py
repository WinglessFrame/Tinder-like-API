from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AnonPermissionsOnly(permissions.BasePermission):
    """
    Non-auth user only
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise PermissionDenied(detail='You have to log out before registration', code=403)
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owner or read-only permission
    """
    message = "You must be an owner to update/delete this item"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
