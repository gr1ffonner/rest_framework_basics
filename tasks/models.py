from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ("manager", "Manager"),
    ("employee", "Employee"),
)


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
