import typing
from ..base import BaseModel
from vkbottle.types import objects

Start = objects.leads.Start


class StartModel(BaseModel):
    response: Start = None


CheckUser = objects.leads.Checked


class CheckUserModel(BaseModel):
    response: CheckUser = None


Complete = objects.leads.Complete


class CompleteModel(BaseModel):
    response: Complete = None


GetStats = objects.leads.Lead


class GetStatsModel(BaseModel):
    response: GetStats = None


GetUsers = typing.List[objects.leads.Entry]


class GetUsersModel(BaseModel):
    response: GetUsers = None


class MetricHit(BaseModel):
    result: bool = None
    redirect_link: str = None


class MetricHitModel(BaseModel):
    response: MetricHit = None
