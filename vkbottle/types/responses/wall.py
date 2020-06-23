import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.wall.Wallpost] = None


class SearchModel(BaseModel):
    response: Search = None


class CreateComment(BaseModel):
    comment_id: int = None


class CreateCommentModel(BaseModel):
    response: CreateComment = None


class Edit(BaseModel):
    post_id: int = None


class EditModel(BaseModel):
    response: Edit = None


GetById = typing.List[objects.wall.WallpostFull]


class GetByIdModel(BaseModel):
    response: GetById = None


class GetComments(BaseModel):
    count: int = None
    items: typing.List[objects.wall.WallComment] = None
    can_post: bool = None
    groups_can_post: bool = None
    current_level_count: int = None


class GetCommentsModel(BaseModel):
    response: GetComments = None


class GetReposts(BaseModel):
    items: typing.List[objects.wall.Wallpost] = None
    profiles: typing.List[objects.users.UserFull] = None
    groups: typing.List[objects.groups.Group] = None


class GetRepostsModel(BaseModel):
    response: GetReposts = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.wall.WallpostFull] = None


class GetModel(BaseModel):
    response: Get = None


class PostAdsStealth(BaseModel):
    post_id: int = None


class PostAdsStealthModel(BaseModel):
    response: PostAdsStealth = None


class Post(BaseModel):
    post_id: int = None


class PostModel(BaseModel):
    response: Post = None


class Repost(BaseModel):
    success: objects.base.OkResponse = None
    post_id: int = None
    reposts_count: int = None
    likes_count: int = None


class RepostModel(BaseModel):
    response: Repost = None
