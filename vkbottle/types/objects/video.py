from . import base
import typing
from ..base import BaseModel


class SaveResult(BaseModel):
    access_key: str = None
    description: str = None
    owner_id: int = None
    title: str = None
    upload_url: str = None
    video_id: int = None


class Video(BaseModel):
    access_key: str = None
    adding_date: int = None
    can_add: "base.BoolInt" = None
    can_comment: "base.BoolInt" = None
    can_edit: "base.BoolInt" = None
    can_like: "base.BoolInt" = None
    can_repost: "base.BoolInt" = None
    comments: int = None
    date: int = None
    description: str = None
    duration: int = None
    files: "VideoFiles" = None
    first_frame: typing.List = None
    height: int = None
    id: int = None
    image: typing.List = None
    is_favorite: bool = None
    live: "base.PropertyExists" = None
    owner_id: int = None
    player: str = None
    processing: "base.PropertyExists" = None
    title: str = None
    type: str = None
    views: int = None
    width: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class VideoAlbumFull(BaseModel):
    count: int = None
    id: int = None
    image: typing.List = None
    is_system: int = None
    owner_id: int = None
    title: str = None
    updated_time: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class VideoFiles(BaseModel):
    external: str = None
    mp4_1080: str = None
    mp4_240: str = None
    mp4_360: str = None
    mp4_480: str = None
    mp4_720: str = None


class VideoFull(BaseModel):
    access_key: str = None
    adding_date: int = None
    can_add: "base.BoolInt" = None
    can_add_to_faves: "base.BoolInt" = None
    can_comment: "base.BoolInt" = None
    can_edit: "base.BoolInt" = None
    can_repost: "base.BoolInt" = None
    comments: int = None
    date: int = None
    description: str = None
    duration: int = None
    files: "VideoFiles" = None
    first_frame: typing.List = None
    first_frame_640: str = None
    first_frame_1280: str = None
    id: int = None
    image: typing.List = None
    likes: "base.Likes" = None
    live: "base.PropertyExists" = None
    owner_id: int = None
    player: str = None
    processing: "base.PropertyExists" = None
    repeat: "base.BoolInt" = None
    title: str = None
    views: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class VideoImage(base.Image):
    with_padding: "base.BoolInt" = None


SaveResult.update_forward_refs()
Video.update_forward_refs()
VideoAlbumFull.update_forward_refs()
VideoFiles.update_forward_refs()
VideoFull.update_forward_refs()
VideoImage.update_forward_refs()
