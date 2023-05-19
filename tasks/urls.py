from django.urls import path
from .views import (
    MessageDetailView,
    MessageListCreateView,
    TaskDetailView,
    TaskListCreateView,
)

urlpatterns = [
    # message's urls
    path("messages/<int:pk>/", MessageDetailView.as_view()),
    path("messages/", MessageListCreateView.as_view()),
    # task's urls
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
    path("tasks/", TaskListCreateView.as_view())
    # users's urls
]
