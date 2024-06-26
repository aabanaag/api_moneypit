"""
Test cases for Order views
"""

import io

import pandas as pd
import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api_moneypit.core.models import BulkOrder
from api_moneypit.core.tests.factories import OrderFactory
from api_moneypit.core.tests.factories import TickerFactory
from api_moneypit.users.tests.factories import UserFactory


@pytest.mark.django_db()
class OrderTestCase(APITestCase):
    def setUp(self):
        super().setUp()

        self.ticker = TickerFactory.create(
            symbol="AAPL", name="Apple Inc.", price=100.00
        )
        TickerFactory.create_batch(9)

        self.ticker.refresh_from_db()

        self.buy_order = {
            "ticker": self.ticker.id,
            "qty": 10,
            "price": 100.00,
            "type": "BUY",
        }

        self.user = UserFactory.create()

    def test_should_not_allow_unauthenticated_user_to_create_order(self):
        url = reverse("api:core:order-list")
        response = self.client.post(url, data=self.buy_order, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_allow_authenticated_user_to_create_order(self):
        self.client.force_login(self.user)

        url = reverse("api:core:order-list")
        response = self.client.post(url, data=self.buy_order, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["ticker"], self.ticker.id)
        self.assertEqual(response.data["qty"], 10)
        self.assertEqual(response.data["price"], "100.00")
        self.assertEqual(response.data["type"], "BUY")
        self.assertEqual(response.data["user"], self.user.id)

    def test_should_not_allow_negative_price(self):
        self.client.force_login(self.user)

        url = reverse("api:core:order-list")
        self.buy_order["price"] = -100
        response = self.client.post(url, data=self.buy_order, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["price"][0],
            "Ensure this value is greater than or equal to 0.0.",
        )

    def test_should_not_allow_negative_qty(self):
        self.client.force_login(self.user)

        url = reverse("api:core:order-list")
        self.buy_order["qty"] = -10
        response = self.client.post(url, data=self.buy_order, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["qty"][0],
            "Ensure this value is greater than or equal to 0.",
        )

    def test_should_update_an_order_status(self):
        self.client.force_login(self.user)

        url = reverse("api:core:order-list")
        response = self.client.post(url, data=self.buy_order, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "PENDING")

        order_id = response.data["id"]

        url = reverse("api:core:order-detail", args=[order_id])
        response = self.client.patch(url, data={"status": "COMPLETED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "COMPLETED")

    def test_should_not_allow_update_if_user_is_not_the_owner(self):
        self.client.force_login(self.user)

        url = reverse("api:core:order-list")
        response = self.client.post(url, data=self.buy_order, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "PENDING")

        order_id = response.data["id"]

        user = UserFactory()
        self.client.force_login(user)

        url = reverse("api:core:order-detail", args=[order_id])
        response = self.client.patch(url, data={"status": "COMPLETED"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_upload_bulk_order(self):
        self.client.force_login(self.user)

        data = {
            "symbol": ["AAPL", "GOOGL", "MSFT"],
            "qty": [10, 20, 30],
            "price": [100.00, 200.00, 300.00],
            "type": ["BUY", "SELL", "BUY"],
        }
        dataframe = pd.DataFrame(data)

        csv_file = io.StringIO()
        dataframe.to_csv(csv_file, index=False)
        csv_file.seek(0)  # Move to the start of the file

        # Create a SimpleUploadedFile object to simulate file upload
        from django.core.files.uploadedfile import SimpleUploadedFile

        uploaded_file = SimpleUploadedFile(
            name="test.csv",
            content=csv_file.getvalue().encode("utf-8"),
            content_type="text/csv",
        )

        url = reverse("api:core:order-bulk-order")
        response = self.client.post(
            url,
            data={"file": uploaded_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["is_processed"])
        self.assertIsNotNone(response.json()["user"])

        bulk_order = BulkOrder.objects.filter(id=response.json()["id"])
        self.assertTrue(bulk_order.exists())

    def test_should_get_total_order(self):
        self.client.force_login(self.user)

        ticker_2 = TickerFactory.create(symbol="GO", name="Google Inc.", price=200.00)

        OrderFactory.create_batch(
            10,
            user=self.user,
            price=100.00,
            qty=10,
            ticker=self.ticker,
            type="BUY",
            status="COMPLETED",
        )
        OrderFactory.create_batch(
            5,
            user=self.user,
            price=100.00,
            qty=10,
            ticker=self.ticker,
            type="SELL",
            status="COMPLETED",
        )
        OrderFactory.create_batch(
            10, user=self.user, price=200.00, qty=10, ticker=ticker_2, type="BUY"
        )

        url = reverse("api:core:order-total-order")
        url = f"{url}?type=BUY&symbol={self.ticker.symbol}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_order"], 10000)

    def test_should_not_get_total_order_for_unauthenticated_user(self):
        url = reverse("api:core:order-total-order")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_get_total_sell_order(self):
        self.client.force_login(self.user)

        OrderFactory.create_batch(
            2,
            user=self.user,
            price=100.00,
            qty=10,
            ticker=self.ticker,
            type="SELL",
            status="COMPLETED",
        )
        OrderFactory.create_batch(
            3,
            user=self.user,
            price=100.00,
            qty=10,
            ticker=self.ticker,
            type="BUY",
            status="COMPLETED",
        )
        OrderFactory.create_batch(
            3, user=self.user, price=200.00, qty=10, ticker=self.ticker, type="BUY"
        )

        url = reverse("api:core:order-total-order")
        url = f"{url}?type=SELL&symbol={self.ticker.symbol}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_order"], 2000)

    def test_should_total_order_for_specific_user(self):
        OrderFactory.create_batch(
            2,
            user=self.user,
            price=100.00,
            qty=10,
            ticker=self.ticker,
            type="SELL",
            status="COMPLETED",
        )
        OrderFactory.create_batch(
            3,
            user=self.user,
            price=100.00,
            qty=10,
            ticker=self.ticker,
            type="BUY",
            status="COMPLETED",
        )

        user_2 = UserFactory()
        ticker = TickerFactory.create(symbol="GO", name="Go", price=100.00)
        OrderFactory.create_batch(
            3,
            user=user_2,
            price=100.00,
            qty=10,
            ticker=ticker,
            type="SELL",
            status="COMPLETED",
        )

        self.client.force_login(user_2)

        url = reverse("api:core:order-total-order")
        url = f"{url}?type=BUY&symbol={self.ticker.symbol}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_order"], 0)
