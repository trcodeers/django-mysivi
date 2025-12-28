from rest_framework.permissions import BasePermission
from .roles import ROLE_PERMISSIONS


class HasPermission(BasePermission):
    """
    Generic role → permission checker
    """

    required_permission = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if not self.required_permission:
            return False

        return self.required_permission in ROLE_PERMISSIONS.get(
            request.user.role,
            set()
        )
