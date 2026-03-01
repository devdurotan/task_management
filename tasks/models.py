from django.db import models
from django.conf import settings
from accounts.models import UserMaster


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        UserMaster,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_by"]),
            models.Index(fields=["completed"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.created_by_id}"