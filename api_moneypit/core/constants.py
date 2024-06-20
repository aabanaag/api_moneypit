from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api_moneypit.core.models import Ticker
    from api_moneypit.users.models import User


@dataclass
class OrderPayload:
    user: "User"
    ticker: "Ticker"
    qty: int
    price: float
    order_type: str
