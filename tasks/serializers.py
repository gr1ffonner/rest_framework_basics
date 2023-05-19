from rest_framework import serializers
from .models import User, Task, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "completed",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "assigned_to" in data and "role" in data["assigned_to"]:
            del data["assigned_to"]["role"]
        return data


class MessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Message
        fields = ["id", "content", "created_by", "created_at"]
