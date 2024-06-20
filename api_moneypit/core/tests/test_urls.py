"""
Test the urls of the core app
"""

import pytest
from django.urls import resolve
from django.urls import reverse

from api_moneypit.core.models import Order
from api_moneypit.core.tests.factories import OrderFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def order() -> Order:
    return OrderFactory()


def test_order_list():
    assert reverse("api:core:order-list") == "/api/orders/"
    assert resolve("/api/orders/").view_name == "api:core:order-list"


def test_order_detail(order: Order):
    assert (
        reverse("api:core:order-detail", kwargs={"pk": order.pk})
        == f"/api/orders/{order.pk}/"
    )
    assert resolve(f"/api/orders/{order.pk}/").view_name == "api:core:order-detail"


def test_bulk_order():
    assert reverse("api:core:order-bulk-order") == "/api/orders/bulk_order/"
    assert resolve("/api/orders/bulk_order/").view_name == "api:core:order-bulk-order"
