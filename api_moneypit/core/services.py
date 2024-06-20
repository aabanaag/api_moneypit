import pandas as pd
from django.db import transaction

from api_moneypit.core.models import BulkOrder
from api_moneypit.core.models import Order
from api_moneypit.core.models import Ticker


def check_and_update_order_status():
    """
    Check if the order status is 'pending' and if it is, change it to 'completed'
    """
    for order in Order.objects.filter(status="PENDING").iterator():
        order.status = "COMPLETED"
        order.save()


def process_bulk_order():
    """
    Check if there are any unprocessed bulk orders
    """
    with transaction.atomic():
        for bulk_order in BulkOrder.objects.filter(is_processed=False).iterator():
            csv_dataframe = pd.read_csv(bulk_order.file, low_memory=True)
            for _, row in csv_dataframe.iterrows():
                try:
                    ticker = Ticker.objects.get(symbol=row["symbol"])
                    Order.objects.create(
                        user=bulk_order.user,
                        ticker=ticker,
                        qty=row["qty"],
                        price=row["price"],
                        type=row["type"],
                    )

                    bulk_order.is_processed = True
                    bulk_order.save()
                except Exception:  # noqa
                    continue
