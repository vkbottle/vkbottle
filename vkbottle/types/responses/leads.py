from .others import SimpleResponse
from ..base import BaseModel


from typing import Any, List


class CheckUserResponse(BaseModel):
    result: bool = None
    reason: str = None
    start_link: str = None
    sid: Any = None


class CheckUser(BaseModel):
    response: CheckUserResponse = None


class CompleteResponse(BaseModel):
    limit: int = None
    day_limit: int = None
    spent: int = None
    cost: str = None
    test_mode: int = None
    success: int = None


class Complete(BaseModel):
    response: CompleteResponse = None


class GetStatsResponseDays(BaseModel):
    impressions: int = None
    started: int = None
    completed: int = None
    spent: int = None


class GetStatsResponse(BaseModel):
    limit: int = None
    spent: int = None
    cost: str = None
    impressions: int = None
    started: int = None
    completed: int = None
    days: List[GetStatsResponseDays] = []


class GetStats(BaseModel):
    response: GetStatsResponse = None


class GetUsersResponse(BaseModel):
    uid: int = None
    aid: int = None
    sid: str = None
    date: int = None
    start_date: int = None
    status: int = None
    test_mode: int = None
    comment: str = None


class GetUsers(BaseModel):
    response: List[GetUsersResponse] = []


class MetricHitResponse(BaseModel):
    result: bool = None
    redirect_link: str = None


class MetricHit(BaseModel):
    response: MetricHitResponse = None


class StartResponse(BaseModel):
    test_mode: int = None
    vk_sid: Any = None


class Start(BaseModel):
    response: StartResponse = None
