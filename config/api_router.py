from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from api_moneypit.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="user")


app_name = "api"
urlpatterns = [
    path("", include("api_moneypit.core.urls")),
    *router.urls,
]
