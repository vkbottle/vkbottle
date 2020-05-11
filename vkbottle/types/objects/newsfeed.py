from . import base, wall, photos
import typing
from enum import Enum
from ..base import BaseModel


class CommentsFilters(Enum):
    post = "post"
    photo = "photo"
    video = "video"
    topic = "topic"
    note = "note"


class EventActivity(BaseModel):
    address: str = None
    button_text: str = None
    friends: typing.List["ItemFriend"] = None
    member_status: int = None
    text: str = None
    time: int = None


class Filters(Enum):
    post = "post"
    photo = "photo"
    photo_tag = "photo_tag"
    wall_photo = "wall_photo"
    friend = "friend"
    note = "note"
    audio = "audio"
    video = "video"


class IgnoreItemType(Enum):
    wall = "wall"
    tag = "tag"
    profilephoto = "profilephoto"
    video = "video"
    photo = "photo"
    audio = "audio"


class ItemAudioAudio(BaseModel):
    count: int = None
    items: typing.List = None


class ItemBase(BaseModel):
    type: "NewsfeedItemType" = None
    source_id: int = None
    date: int = None


class ItemAudio(ItemBase):
    audio: "ItemAudioAudio" = None
    post_id: int = None


class ItemDigest(ItemBase):
    button_text: str = None
    feed_id: str = None
    items: typing.List = None
    main_post_ids: typing.List = None
    template: str = None
    title: str = None
    track_code: str = None


class ItemFriend(ItemBase):
    friends: "ItemFriendFriends" = None


class ItemFriendFriends(BaseModel):
    count: int = None
    items: typing.List = None


class ItemNote(ItemBase):
    notes: "ItemNoteNotes" = None


class ItemNoteNotes(BaseModel):
    count: int = None
    items: typing.List = None


class ItemPhoto(ItemBase):
    photos: "ItemPhotoPhotos" = None
    post_id: int = None


class ItemPhotoPhotos(BaseModel):
    count: int = None
    items: typing.List = None


class ItemPhotoTag(ItemBase):
    photo_tags: "ItemPhotoTagPhotoTags" = None
    post_id: int = None


class ItemPhotoTagPhotoTags(BaseModel):
    count: int = None
    items: typing.List = None


class ItemStoriesBlock(ItemBase):
    block_type: str = None
    stories: typing.List = None
    title: str = None
    track_code: str = None


class ItemTopic(ItemBase):
    comments: "base.CommentsInfo" = None
    likes: "base.LikesInfo" = None
    post_id: int = None
    text: str = None


class ItemVideo(ItemBase):
    video: "ItemVideoVideo" = None


class ItemVideoVideo(BaseModel):
    count: int = None
    items: typing.List = None


class ItemWallpost(ItemBase):
    activity: "EventActivity" = None
    attachments: typing.List = None
    comments: "base.CommentsInfo" = None
    copy_history: typing.List = None
    geo: "base.Geo" = None
    likes: "base.LikesInfo" = None
    post_id: int = None
    post_source: "wall.PostSource" = None
    post_type: "ItemWallpostType" = None
    reposts: "base.RepostsInfo" = None
    text: str = None


class ItemWallpostType(Enum):
    post = "post"
    copy = "copy"
    reply = "reply"


class List(BaseModel):
    id: int = None
    title: str = None


class ListFull(List):
    no_reposts: "base.BoolInt" = None
    source_ids: typing.List = None


class NewsfeedItemType(Enum):
    post = "post"
    photo = "photo"
    photo_tag = "photo_tag"
    wall_photo = "wall_photo"
    friend = "friend"
    note = "note"
    audio = "audio"
    video = "video"
    topic = "topic"
    digest = "digest"
    stories = "stories"


class NewsfeedNote(BaseModel):
    comments: int = None
    id: int = None
    owner_id: int = None
    title: str = None


class NewsfeedPhoto(photos.Photo):
    likes: "base.Likes" = None
    comments: "base.ObjectCount" = None
    can_comment: "base.BoolInt" = None
    can_repost: "base.BoolInt" = None


EventActivity.update_forward_refs()
ItemAudio.update_forward_refs()
ItemAudioAudio.update_forward_refs()
ItemBase.update_forward_refs()
ItemDigest.update_forward_refs()
ItemFriend.update_forward_refs()
ItemFriendFriends.update_forward_refs()
ItemNote.update_forward_refs()
ItemNoteNotes.update_forward_refs()
ItemPhoto.update_forward_refs()
ItemPhotoPhotos.update_forward_refs()
ItemPhotoTag.update_forward_refs()
ItemPhotoTagPhotoTags.update_forward_refs()
ItemStoriesBlock.update_forward_refs()
ItemTopic.update_forward_refs()
ItemVideo.update_forward_refs()
ItemVideoVideo.update_forward_refs()
ItemWallpost.update_forward_refs()
List.update_forward_refs()
ListFull.update_forward_refs()
NewsfeedNote.update_forward_refs()
NewsfeedPhoto.update_forward_refs()
