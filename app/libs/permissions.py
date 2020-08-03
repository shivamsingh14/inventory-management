from rest_framework import permissions

from app.stores.models import User


class StaffPermissions(permissions.BasePermission):
    """
    permission class that return strue if user has admin rights
    """

    def has_permission(self, request, view):
        return request.user.is_staff

class OwnerPermission(permissions.BasePermission):
    """
    permission class that return strue if user has admin rights
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
