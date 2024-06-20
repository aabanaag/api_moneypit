"""
Core factories
"""

from factory import Faker
from factory import Iterator
from factory import SubFactory
from factory.django import DjangoModelFactory

from api_moneypit.core.models import Order
from api_moneypit.core.models import Ticker


class TickerFactory(DjangoModelFactory):
    symbol = Faker("swift", length=8)
    name = Faker("company")
    price = Faker("pyfloat", positive=True, max_value=1000.0)

    class Meta:
        model = Ticker
        django_get_or_create = ("symbol",)


class OrderFactory(DjangoModelFactory):
    user = SubFactory("api_moneypit.users.tests.factories.UserFactory")
    ticker = SubFactory(TickerFactory)
    qty = Faker("random_int", min=1, max=100)
    price = Faker("pyfloat", positive=True, max_value=1000.0)
    type = Iterator(Order.ORDER_TYPE_CHOICES, getter=lambda c: c[0])
    status = Iterator(Order.ORDER_STATUS_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Order
