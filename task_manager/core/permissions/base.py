from rest_framework.permissions import BasePermission
from .roles import ROLE_PERMISSIONS


class HasPermission(BasePermission):
    """
    Generic role → permission checker
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        required_permission = getattr(view, "required_permission", None)
        if not required_permission:
            return False

        return required_permission in ROLE_PERMISSIONS.get(
            request.user.role,
            set()
        )
