from django.urls import path
from core.views.auth import FreeResourceAPIView, LoginAPIView, LogoutAPIView, ManagerSignupAPIView, MeAPIView
from core.views.user import CreateReporteeAPIView
from core.views.task import TaskAssignAPIView, TaskCreateAPIView, TaskDeleteAPIView, TaskListAPIView, TaskStatusByManagerAPIView, TaskStatusByReporteeAPIView

urlpatterns = [
    path("auth/signup", ManagerSignupAPIView.as_view()), # TO SIGN UP manager
    path("auth/login", LoginAPIView.as_view()), # TO LOGIN
    path("auth/logout", LogoutAPIView.as_view()), # TO LOGOUT
    path("auth/me", MeAPIView.as_view()),    # TO GET LOGGED IN USER DETAILS
    path("users/reportees", CreateReporteeAPIView.as_view()), # TO CREATE REPORTEE by manager only

    path("tasks", TaskListAPIView.as_view()), # TO LIST TASKS reportee/manager
    path("tasks/create", TaskCreateAPIView.as_view()), # TO CREATE TASK by manager only
    path("tasks/<int:task_id>/assign", TaskAssignAPIView.as_view()), # TO ASSIGN TASK by manager only to reportee created by them only
    path("tasks/<int:task_id>", TaskDeleteAPIView.as_view()), # TO DELETE TASK by manager only
    path("tasks/<int:task_id>/status", TaskStatusByManagerAPIView.as_view()), # TO UPDATE TASK STATUS by manager only
    path("tasks/<int:task_id>/self", TaskStatusByReporteeAPIView.as_view()), # TO UPDATE OWN TASK STATUS by reportee only 

    path("free-resource", FreeResourceAPIView.as_view()),  # New free resource endpoint with no authentication, ignore it
]
