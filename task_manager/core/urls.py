from django.urls import path
from core.views.auth import FreeResourceAPIView, LoginAPIView, LogoutAPIView, ManagerSignupAPIView, MeAPIView
from core.views.user import CreateReporteeAPIView
from core.views.task import TaskAssignAPIView, TaskCreateAPIView, TaskDeleteAPIView, TaskListAPIView, TaskStatusByManagerAPIView, TaskStatusByReporteeAPIView

urlpatterns = [
    path("auth/signup", ManagerSignupAPIView.as_view()),
    path("auth/login", LoginAPIView.as_view()),
    path("auth/logout", LogoutAPIView.as_view()),
    path("auth/me", MeAPIView.as_view()),   
    path("users/reportees", CreateReporteeAPIView.as_view()),

    path("tasks", TaskListAPIView.as_view()),
    path("tasks/create", TaskCreateAPIView.as_view()),
    path("tasks/<int:task_id>/assign", TaskAssignAPIView.as_view()),
    path("tasks/<int:task_id>", TaskDeleteAPIView.as_view()),
    path("tasks/<int:task_id>/status", TaskStatusByManagerAPIView.as_view()),
    path("tasks/<int:task_id>/self", TaskStatusByReporteeAPIView.as_view()),

    path("free-resource", FreeResourceAPIView.as_view()),  # New free resource endpoint
]
