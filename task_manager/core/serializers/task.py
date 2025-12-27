from rest_framework import serializers
from core.models import Task, User


class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    assigned_to_id = serializers.IntegerField(required=False)


class TaskAssignSerializer(serializers.Serializer):
    assigned_to_id = serializers.IntegerField()


class TaskStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["DEV", "TEST", "STUCK", "COMPLETED"]
    )
