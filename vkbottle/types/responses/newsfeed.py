import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    total_count: int = None
    count: int = None
    next_from: str = None
    items: typing.List[objects.wall.Wallpost] = None


class SearchModel(BaseModel):
    response: Search = None


class GetBanned(BaseModel):
    groups: typing.List[objects.groups.Group] = None
    members: typing.List[objects.users.User] = None
    profiles: typing.List[objects.users.User] = None


class GetBannedModel(BaseModel):
    response: GetBanned = None


class GetComments(BaseModel):
    items: typing.List[objects.wall.Wallpost] = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None
    next_from: str = None


class GetCommentsModel(BaseModel):
    response: GetComments = None


class WallpostList(BaseModel):
    id: int = None
    title: str = None


class GetLists(BaseModel):
    count: int = None
    items: typing.List[WallpostList] = None
    no_reposts: bool = None
    source_ids: typing.List[int] = None


class GetListsModel(BaseModel):
    response: GetLists = None


class GetMentions(BaseModel):
    count: int = None
    items: typing.List[objects.wall.Wallpost] = None


class GetMentionsModel(BaseModel):
    response: GetMentions = None


class GetRecommended(BaseModel):
    items: typing.List[objects.wall.Wallpost] = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None
    new_offset: str = None
    next_from: str = None


class GetRecommendedModel(BaseModel):
    response: GetRecommended = None


class GetSuggestedSources(BaseModel):
    count: int = None
    items: typing.List[objects.groups.Group] = None


class GetSuggestedSourcesModel(BaseModel):
    response: GetSuggestedSources = None


class Get(BaseModel):
    items: typing.List[objects.wall.Wallpost] = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None
    next_from: str = None


class GetModel(BaseModel):
    response: Get = None


SaveList = typing.Dict


class SaveListModel(BaseModel):
    response: SaveList = None
