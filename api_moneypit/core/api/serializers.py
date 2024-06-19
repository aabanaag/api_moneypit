from rest_framework import serializers

from api_moneypit.core.models import Order
from api_moneypit.core.models import Ticker
from api_moneypit.users.api.serializers import UserSerializer


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = "__all__"


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "ticker", "qty", "price", "type", "user", "status")
        extra_kwargs = {
            "user": {"required": False},
            "id": {"read_only": True},
        }


class OrderRetrieveSerializer(serializers.ModelSerializer):
    ticker = TickerSerializer()
    user = UserSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
