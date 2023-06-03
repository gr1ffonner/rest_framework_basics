from django.core.exceptions import PermissionDenied
from .models import Task, Message, User
from dj_rest_auth.registration.views import RegisterView
from rest_framework import permissions, viewsets
from .serializers import (
    TaskSerializer,
    MessageSerializer,
    UserSerializer,
    CustomRegisterSerializer,
)
from .permissions import IsManagerOrReadOnly, IsEmployeeOrReadOnly


class CustomRegisterView(RegisterView):
    """Регистрация пользователя с выбором роли (кроме админа)"""

    serializer_class = CustomRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Список пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (permissions.IsAdminUser,)


class MessageViewSet(viewsets.ModelViewSet):
    """Сообщения"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsManagerOrReadOnly | permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """Таски"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        IsManagerOrReadOnly | IsEmployeeOrReadOnly | permissions.IsAdminUser
    ]

    def create(self, request, *args, **kwargs):
        if request.user.role == "employee":
            raise PermissionDenied("You are not allowed to create tasks.")
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == "employee":
                return Task.objects.filter(assigned_to=user)
            return Task.objects.all()
        return Task.objects.none()  # Return empty queryset for unauthenticated users

    def perform_create(self, serializer):
        assigned_to_username = self.request.data.get("assigned_to")
        assigned_to = User.objects.get(username=assigned_to_username)
        if self.request.user.role == "employee" and self.request.user != assigned_to:
            raise PermissionDenied("You are not allowed to assign tasks to others.")

        completed = self.request.data.get(
            "completed", False
        )  # Get the completed value from the request data
        serializer.save(assigned_to=assigned_to, completed=completed)
