from .models import Task, Message, User
from dj_rest_auth.registration.views import RegisterView
from rest_framework import generics, permissions, viewsets
from .serializers import (
    TaskSerializer,
    MessageSerializer,
    UserSerializer,
    CustomRegisterSerializer,
)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (permissions.IsAdminUser,)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        assigned_to_username = self.request.data.get("assigned_to")
        assigned_to = User.objects.get(username=assigned_to_username)
        serializer.save(assigned_to=assigned_to)
