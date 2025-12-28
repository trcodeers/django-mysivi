from math import ceil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.models import Task, User
from core.serializers.task import (
    TaskCreateSerializer,
    TaskAssignSerializer,
    TaskStatusUpdateSerializer,
)
from core.throttles import TaskCreateRateThrottle, TaskListRateThrottle
from core.permissions.base import HasPermission
from core.authentication import CsrfExemptSessionAuthentication
from core.config import TASK_LIST_PAGINATION_SIZE

class TaskListAPIView(APIView):
    throttle_classes = [TaskListRateThrottle]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  

        page = int(request.query_params.get("page", 1))
        offset = (page - 1) * TASK_LIST_PAGINATION_SIZE

        # if it is a manager, fetch tasks created by them
        if user.role == "MANAGER":
            qs = Task.objects.filter(
                created_by=user,            
                company=user.company,       
                is_deleted=False
            )
        # if it is a reportee, fetch tasks assigned to them 
        elif user.role == "REPORTEE":
            qs = Task.objects.filter(
                assigned_to=user,          
                company=user.company,       
                is_deleted=False
            )

        else:
            return Response(
                {"detail": "Invalid role"},
                status=403
            )

        total_tasks = qs.count()
        max_page = max(1, ceil(total_tasks / TASK_LIST_PAGINATION_SIZE))

        if page > max_page:
            return Response(
                {
                    "detail": f"Page {page} does not exist. "
                              f"Max page is {max_page}."
                },
                status=404
            )

        tasks = (
            qs.order_by("-created_at")
              [offset: offset + TASK_LIST_PAGINATION_SIZE]
        )

        return Response({
            "page": page,
            "page_size": TASK_LIST_PAGINATION_SIZE,
            "total_tasks": total_tasks,
            "max_page": max_page,
            "tasks": [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "assigned_to_id": task.assigned_to_id,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                }
                for task in tasks
            ]
        })


class TaskCreateAPIView(APIView):
    throttle_classes = [TaskCreateRateThrottle]
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [HasPermission]
    required_permission = "task:create"

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        manager = request.user  # MUST be the loggedin manager

        assigned_to = None
        assigned_to_id = serializer.validated_data.get("assigned_to_id")

        # Validate reportee if assignment is requested
        if assigned_to_id is not None:
            assigned_to = User.objects.filter(
                id=assigned_to_id,
                role="REPORTEE",
                company=manager.company,   #  same company
                manager=manager            #  created by THIS manager
            ).first()

            if not assigned_to:
                return Response(
                    {"detail": "Invalid reportee for this manager or company"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create task under THIS manager & company
        task = Task.objects.create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            assigned_to=assigned_to,
            created_by=manager,           #  ownership enforced
            company=manager.company       #  tenant isolation
        )

        return Response(
            {
                "id": task.id,
                "assigned_to_id": assigned_to.id if assigned_to else None,
                "message": "Task created successfully",
            },
            status=status.HTTP_201_CREATED
        )


class TaskAssignAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [HasPermission]
    required_permission = "task:assign"

    def patch(self, request, task_id):
        serializer = TaskAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        manager = request.user  

        #  Fetch task created by THIS manager in SAME company
        task = Task.objects.filter(
            id=task_id,
            created_by=manager,         
            company=manager.company,    
            is_deleted=False
        ).first()

        if not task:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        #  Fetch reportee from SAME company
        reportee = User.objects.filter(
            id=serializer.validated_data["assigned_to_id"],
            role="REPORTEE",
            company=manager.company     
        ).first()

        if not reportee:
            return Response(
                {"detail": "Invalid reportee for this company"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Assign / reassign task
        task.assigned_to = reportee
        task.save(update_fields=["assigned_to", "updated_at"])

        return Response(
            {
                "task_id": task.id,
                "assigned_to_id": reportee.id,
                "message": "Task assigned successfully",
            },
            status=status.HTTP_200_OK
        )


class TaskDeleteAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [HasPermission]
    required_permission = "task:delete"

    def delete(self, request, task_id):
        manager = User.objects.filter(role="MANAGER").first()

        task = Task.objects.filter(
            id=task_id,
            created_by=manager,
            is_deleted=False
        ).first()

        if not task:
            return Response({"detail": "Task not found"}, status=404)

        task.is_deleted = True
        task.save()

        return Response({
            "task_id": task.id,
            "message": "Task deleted successfully"
        })


class TaskStatusByManagerAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [HasPermission]
    required_permission = "task:update:any"

    def patch(self, request, task_id):
        serializer = TaskStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        manager = request.user  # ✅ FIX

        task = Task.objects.filter(
            id=task_id,
            created_by=manager,           
            company=manager.company,      
            is_deleted=False
        ).first()

        if not task:
            return Response(
                {"detail": "Task not found"},
                status=404
            )

        task.status = serializer.validated_data["status"]
        task.save(update_fields=["status", "updated_at"])

        return Response({
            "task_id": task.id,
            "new_status": task.status,
            "message": "Task status updated successfully"
        })



class TaskStatusByReporteeAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [HasPermission]
    required_permission = "task:update:self"

    def patch(self, request, task_id):
        serializer = TaskStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reportee = request.user

        task = Task.objects.filter(
            id=task_id,
            assigned_to=reportee,         
            company=reportee.company,     
            is_deleted=False
        ).first()

        if not task:
            return Response(
                {"detail": "Task not found"},
                status=404
            )

        if task.status == "COMPLETED":
            return Response(
                {"detail": "Task is already completed"},
                status=409
            )

        if serializer.validated_data["status"] != "COMPLETED":
            return Response(
                {"detail": "Reportee can update task status only to COMPLETED"},
                status=403
            )

        task.status = "COMPLETED"
        task.save(update_fields=["status", "updated_at"])

        return Response({
            "task_id": task.id,
            "new_status": task.status,
            "message": "Task status updated successfully"
        })
