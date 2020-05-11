import typing
from ..base import BaseModel


class Search(BaseModel):
    items: typing.List = None
    suggested_queries: typing.List = None


class SearchModel(BaseModel):
    response: Search = None


class GetBanned(BaseModel):
    groups: typing.List = None
    members: typing.List = None


class GetBannedModel(BaseModel):
    response: GetBanned = None


class GetComments(BaseModel):
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None
    next_from: str = None


class GetCommentsModel(BaseModel):
    response: GetComments = None


class GetLists(BaseModel):
    count: int = None
    items: typing.List = None


class GetListsModel(BaseModel):
    response: GetLists = None


class GetMentions(BaseModel):
    count: int = None
    items: typing.List = None


class GetMentionsModel(BaseModel):
    response: GetMentions = None


class GetRecommended(BaseModel):
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None
    new_offset: str = None
    next_from: str = None


class GetRecommendedModel(BaseModel):
    response: GetRecommended = None


class GetSuggestedSources(BaseModel):
    count: int = None
    items: typing.List = None


class GetSuggestedSourcesModel(BaseModel):
    response: GetSuggestedSources = None


class Get(BaseModel):
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None
    next_from: str = None


class GetModel(BaseModel):
    response: Get = None


SaveList = typing.Dict


class SaveListModel(BaseModel):
    response: SaveList = None
