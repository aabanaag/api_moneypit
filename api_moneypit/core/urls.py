"""
Core - Urls
"""

from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from api_moneypit.core.api.views import OrderViewSet
from api_moneypit.core.api.views import TickerViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("orders", OrderViewSet, basename="order")
router.register("tickers", TickerViewSet, basename="ticker")

app_name = "core"
urlpatterns = router.urls
