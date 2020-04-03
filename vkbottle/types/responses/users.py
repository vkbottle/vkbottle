from .others import SimpleResponse
from ..base import BaseModel
from ..user import User
from enum import Enum
import typing


class Get(BaseModel):
    response: typing.List[User] = None


class GetFollowers(Get):
    pass


class SubscriptionType(Enum):
    profile = "profile"
    page = "page"


class Subscription(BaseModel):
    id: int = None
    type: SubscriptionType = None

    name: str = None
    screen_name: str = None
    is_closed: typing.Union[int, bool] = None

    first_name: str = None
    last_name: str = None
    can_access_closed: bool = None

    is_admin: int = None
    is_member: int = None
    is_advertiser: int = None

    photo_50: str = None
    photo_100: str = None
    photo_200: str = None


class SubscriptionUsers(BaseModel):
    count: int = None
    items: typing.List[int] = None


class SubscriptionGroups(BaseModel):
    count: int = None
    items: typing.List[int] = None


class GetSubscriptionsResponse(BaseModel):
    items: typing.List[Subscription] = None
    users: SubscriptionUsers = None
    groups: SubscriptionGroups = None


class GetSubscriptions(BaseModel):
    response: GetSubscriptionsResponse = None


class Report(SimpleResponse):
    pass


class Search(Get):
    pass
