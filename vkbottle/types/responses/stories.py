import typing
from ..base import BaseModel
from vkbottle.types import objects


class Upload(BaseModel):
    story: objects.stories.Story = None


class UploadModel(BaseModel):
    response: Upload = None


class GetBanned(BaseModel):
    count: int = None
    items: typing.List = None


class GetBannedModel(BaseModel):
    response: GetBanned = None


class GetById(BaseModel):
    count: int = None
    items: typing.List = None


class GetByIdModel(BaseModel):
    response: GetById = None


class GetPhotoUploadServer(BaseModel):
    upload_url: str = None
    user_ids: typing.List = None


class GetPhotoUploadServerModel(BaseModel):
    response: GetPhotoUploadServer = None


class GetReplies(BaseModel):
    count: int = None
    items: typing.List = None


class GetRepliesModel(BaseModel):
    response: GetReplies = None


GetStats = objects.stories.StoryStats


class GetStatsModel(BaseModel):
    response: GetStats = None


class GetVideoUploadServer(BaseModel):
    upload_url: str = None
    user_ids: typing.List = None


class GetVideoUploadServerModel(BaseModel):
    response: GetVideoUploadServer = None


class GetViewers(BaseModel):
    count: int = None
    items: typing.List = None


class GetViewersModel(BaseModel):
    response: GetViewers = None


class Get(BaseModel):
    count: int = None
    items: typing.List = None
    promo_data: objects.stories.PromoBlock = None


class GetModel(BaseModel):
    response: Get = None
