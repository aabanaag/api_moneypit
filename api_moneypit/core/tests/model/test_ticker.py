"""
Ticker model test
"""

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.db.utils import IntegrityError

from api_moneypit.core.models import Ticker
from api_moneypit.core.tests.factories import TickerFactory

pytestmark = pytest.mark.django_db


def test_should_create_ticker():
    price = 100
    ticker = TickerFactory.create(
        symbol="AAPL",
        name="Apple Inc.",
        price=price,
    )

    assert ticker.symbol == "AAPL"
    assert ticker.name == "Apple Inc."
    assert ticker.price == price


def test_should_not_allow_duplicate_ticker():
    price = 100
    Ticker.objects.create(
        symbol="AAPL",
        name="Apple Inc.",
        price=price,
    )

    with pytest.raises(IntegrityError):
        Ticker.objects.create(
            symbol="AAPL",
            name="Apple Inc.",
            price=price,
        )


def test_should_not_allow_price_with_more_than_ten_digits():
    with pytest.raises(DataError):
        Ticker.objects.create(
            symbol="AAPL",
            name="Apple Inc.",
            price=100000000000.0,
        )


def test_should_not_allow_negative_price():
    with pytest.raises(ValidationError):
        ticker = Ticker.objects.create(
            symbol="AAPL",
            name="Apple Inc.",
            price=-100.0,
        )
        ticker.full_clean()
