import typing
from ..base import BaseModel
from vkbottle.types import objects

UpdateSubscription = objects.base.BoolInt


class UpdateSubscriptionModel(BaseModel):
    response: UpdateSubscription = None


CancelSubscription = objects.base.BoolInt


class CancelSubscriptionModel(BaseModel):
    response: CancelSubscription = None


ChangeState = typing.Dict


class ChangeStateModel(BaseModel):
    response: ChangeState = None


GetAmount = objects.orders.Amount


class GetAmountModel(BaseModel):
    response: GetAmount = None


GetById = typing.List[objects.orders.Order]


class GetByIdModel(BaseModel):
    response: GetById = None


GetUserSubscriptionById = objects.orders.Subscription


class GetUserSubscriptionByIdModel(BaseModel):
    response: GetUserSubscriptionById = None


GetUserSubscriptions = objects.orders.Subscription


class GetUserSubscriptionsModel(BaseModel):
    response: GetUserSubscriptions = None


Get = typing.List[objects.orders.Order]


class GetModel(BaseModel):
    response: Get = None
