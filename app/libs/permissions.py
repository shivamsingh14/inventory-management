from rest_framework import permissions

from app.stores.models import User


class StaffPermissions(permissions.BasePermission):
    """
    permission class that return strue if user has admin rights
    """

    def has_permission(self, request, view):
        return request.user.is_staff
