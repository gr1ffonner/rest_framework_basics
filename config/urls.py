from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from tasks.views import CustomRegisterView
from dj_rest_auth.registration.views import VerifyEmailView

schema_view = get_schema_view(
    openapi.Info(
        title="TASKS API",
        default_version="v1",
        description="A sample API for task and message management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="privetpoka@example.com"),
        license=openapi.License(name="Danya License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("tasks.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "api/v1/dj-rest-auth/registration/",
        CustomRegisterView.as_view(),
        name="rest_register",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
