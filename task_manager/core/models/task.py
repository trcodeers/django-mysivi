# core/models/task.py
from django.db import models
from .user import User
from .company import Company

class Task(models.Model):
    STATUS_CHOICES = (
        ("DEV", "Development"),
        ("TEST", "Testing"),
        ("STUCK", "Stuck"),
        ("COMPLETED", "Completed"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DEV"
    )

    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title