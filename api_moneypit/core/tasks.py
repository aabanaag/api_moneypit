from celery import shared_task

from api_moneypit.core.services import check_and_update_order_status
from api_moneypit.core.services import process_bulk_order


@shared_task
def check_order_status():
    """
    Check if the order status is 'pending' and if it is, change it to 'completed'
    """
    check_and_update_order_status()


@shared_task
def check_bulk_order():
    """
    Check if there are any unprocessed bulk orders
    """
    process_bulk_order()
