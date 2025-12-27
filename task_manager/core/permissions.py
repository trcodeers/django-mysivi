from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MANAGER"

class IsReportee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "REPORTEE"
