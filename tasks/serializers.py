from rest_framework import serializers
from .models import User, Task, Message
from .models import ROLE_CHOICES
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "role",
        )

    # override get_cleaned_data of RegisterSerializer
    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "role": self.validated_data.get("role", ""),
        }

    # override save method of RegisterSerializer
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.role = self.cleaned_data.get("role")
        user.save()
        adapter.save_user(request, user, self)
        return user


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
