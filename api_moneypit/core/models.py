import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from api_moneypit.core.constants import OrderPayload

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ticker(BaseModel):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return self.symbol


class Order(BaseModel):
    ORDER_STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    ORDER_TYPE_CHOICES = (
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="orders")
    qty = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="PENDING",
    )
    type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default="BUY")

    def __str__(self):
        return f"({self.id}) - {self.type}: {self.ticker.symbol}"

    @classmethod
    def create_order(cls, payload: OrderPayload):
        return cls.objects.create(
            user=payload.user,
            ticker=payload.ticker,
            qty=payload.qty,
            price=payload.price,
            type=payload.order_type,
        )


class BulkOrder(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bulk_orders",
    )
    file = models.FileField(upload_to="bulk_orders/")
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.id}) - {self.file.name}"
