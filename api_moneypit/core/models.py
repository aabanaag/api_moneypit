from django.db import models
from django.conf import settings
import uuid

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ticker(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.symbol


class Order(BaseModel):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name='orders')
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.ticker.symbol} - {self.qty} - {self.price} - {self.status}"

    @classmethod
    def create_order(cls, user, ticker, qty, price):
        return cls.objects.create(
            user=user,
            ticker=ticker,
            qty=qty,
            price=price
        )

