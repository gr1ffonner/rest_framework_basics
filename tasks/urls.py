from rest_framework.routers import SimpleRouter
from .views import (
    UserViewSet,
    MessageViewSet,
    TaskViewSet,
)

router = SimpleRouter()


router.register(r"users", UserViewSet, basename="users")
router.register("tasks", TaskViewSet, basename="tasks")
router.register("messages", MessageViewSet, basename="messages")
urlpatterns = router.urls
