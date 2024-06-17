"""
Core - Urls
"""

from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from api_moneypit.core.api.views import OrderViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("orders", OrderViewSet, basename="order")

url_patterns = router.urls
