from api_moneypit.core.models import Order, Ticker
from api_moneypit.users.api.serializers import UserSerializer

from rest_framework.exceptions import ValidationError
from rest_framework import serializers


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = '__all__'


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(write_only=True, required=True)

    def validate_symbol(self, value): # noqa
        if not Ticker.objects.filter(symbol=value).exists():
            raise ValidationError("Invalid ticker symbol")

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        symbol = validated_data.pop('symbol')
        ticker = Ticker.objects.get(symbol=symbol)
        return Order.create_order(
            user=self.context['request'].user,
            ticker=ticker,
            **validated_data
        )

    def update(self, instance, validated_data):
        symbol = validated_data.pop('symbol')
        ticker = Ticker.objects.get(symbol=symbol)
        instance.ticker = ticker
        instance.qty = validated_data.get('qty', instance.qty)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class OrderRetrieveSerializer(serializers.ModelSerializer):
    ticker = TickerSerializer()
    user = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
