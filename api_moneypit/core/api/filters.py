from django_filters import CharFilter
from django_filters import ChoiceFilter
from django_filters import FilterSet

from api_moneypit.core.models import Order


class OrderFilter(FilterSet):
    type = ChoiceFilter(choices=Order.ORDER_TYPE_CHOICES, field_name="type")
    status = ChoiceFilter(choices=Order.ORDER_STATUS_CHOICES, field_name="status")
    symbol = CharFilter(field_name="ticker__symbol", lookup_expr="exact")

    class Meta:
        model = Order
        fields = ("type", "status", "symbol")
