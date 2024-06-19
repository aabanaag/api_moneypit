"""
Core - Urls
"""

from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from api_moneypit.core.api.views import OrderViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("orders", OrderViewSet, basename="order")

app_name = "core"
urlpatterns = router.urls
