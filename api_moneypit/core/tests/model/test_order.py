"""
Order model tests
"""

import pytest
from django.db import IntegrityError

from api_moneypit.core.constants import OrderPayload
from api_moneypit.core.models import Order
from api_moneypit.core.tests.factories import OrderFactory
from api_moneypit.core.tests.factories import TickerFactory

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("user")
def test_order_creation(user):
    """
    Test order creation
    """
    qty = 10
    price = 100

    ticker = TickerFactory.create(symbol="AAPL", name="Apple Inc.")
    order = OrderFactory.create(ticker=ticker, user=user, qty=qty, price=price)

    assert order.id is not None
    assert order.user == user
    assert order.ticker == ticker
    assert order.qty == qty
    assert order.price == price
    assert order.status == "PENDING"
    assert order.type == "BUY"


def test_should_not_create_order_without_user():
    """
    Test order creation without user
    """
    ticker = TickerFactory.create(symbol="AAPL", name="Apple Inc.")
    with pytest.raises(IntegrityError):
        OrderFactory.create(ticker=ticker, qty=15, price=105.0, user=None)


@pytest.mark.usefixtures("user")
def test_should_not_create_order_without_ticker(user):
    """
    Test order creation without ticker
    """
    with pytest.raises(IntegrityError):
        OrderFactory.create(user=user, qty=12, price=107.0, ticker=None)


@pytest.mark.usefixtures("user")
def test_should_update_status_to_completed(user):
    """
    Test order status update
    """
    ticker = TickerFactory.create(symbol="AAPL", name="Apple Inc.")
    order = OrderFactory.create(ticker=ticker, user=user, qty=16, price=20.0)

    # Check if order status is pending
    assert order.status == "PENDING"

    # update status to completed
    order.status = "COMPLETED"
    order.save()

    order.refresh_from_db()

    assert order.status == "COMPLETED"


@pytest.mark.usefixtures("user")
def test_should_create_sell_order(user):
    """
    Test sell order creation
    """
    ticker = TickerFactory.create(symbol="AAPL", name="Apple Inc.")

    qty = 78
    price = 500.0
    payload = OrderPayload(
        user=user,
        ticker=ticker,
        qty=qty,
        price=price,
        order_type="SELL",
    )
    order = Order.create_order(payload=payload)

    assert order.user == user
    assert order.ticker == ticker
    assert order.qty == qty
    assert order.price == price
    assert order.type == "SELL"
