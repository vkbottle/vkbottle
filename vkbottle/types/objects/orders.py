import typing
from ..base import BaseModel


class Amount(BaseModel):
    amounts: typing.List = None
    currency: str = None


class AmountItem(BaseModel):
    amount: int = None
    description: str = None
    votes: str = None


class Order(BaseModel):
    amount: int = None
    app_order_id: int = None
    cancel_transaction_id: int = None
    date: int = None
    id: int = None
    item: str = None
    receiver_id: int = None
    status: str = None
    transaction_id: int = None
    user_id: int = None


class Subscription(BaseModel):
    cancel_reason: str = None
    create_time: int = None
    id: int = None
    item_id: str = None
    next_bill_time: int = None
    pending_cancel: bool = None
    period: int = None
    period_start_time: int = None
    price: int = None
    status: str = None
    test_mode: bool = None
    trial_expire_time: int = None
    update_time: int = None


Amount.update_forward_refs()
AmountItem.update_forward_refs()
Order.update_forward_refs()
Subscription.update_forward_refs()
