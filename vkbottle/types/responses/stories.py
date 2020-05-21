import typing
from ..base import BaseModel
from vkbottle.types import objects


class Upload(BaseModel):
    story: objects.stories.Story = None


class UploadModel(BaseModel):
    response: Upload = None


class GetBanned(BaseModel):
    count: int = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None


class GetBannedModel(BaseModel):
    response: GetBanned = None


class GetById(BaseModel):
    count: int = None
    items: typing.List[objects.stories.Story] = None


class GetByIdModel(BaseModel):
    response: GetById = None


class GetPhotoUploadServer(BaseModel):
    upload_url: str = None
    user_ids: typing.List[int] = None


class GetPhotoUploadServerModel(BaseModel):
    response: GetPhotoUploadServer = None


class GetReplies(BaseModel):
    count: int = None
    items: typing.List[objects.stories.Replies] = None


class GetRepliesModel(BaseModel):
    response: GetReplies = None


GetStats = objects.stories.StoryStats


class GetStatsModel(BaseModel):
    response: GetStats = None


class GetVideoUploadServer(BaseModel):
    upload_url: str = None
    user_ids: typing.List[int] = None


class GetVideoUploadServerModel(BaseModel):
    response: GetVideoUploadServer = None


class GetViewers(BaseModel):
    count: int = None
    items: typing.List[int] = None


class GetViewersModel(BaseModel):
    response: GetViewers = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.stories.Story] = None
    promo_data: objects.stories.PromoBlock = None


class GetModel(BaseModel):
    response: Get = None
