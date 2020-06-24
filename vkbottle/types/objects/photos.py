from . import base, comment
import typing
from enum import Enum
from ..base import BaseModel


class CommentXtrPid(BaseModel):
    attachments: typing.List = None
    date: int = None
    from_id: int = None
    id: int = None
    likes: "base.LikesInfo" = None
    pid: int = None
    reply_to_comment: int = None
    reply_to_user: int = None
    text: str = None
    parents_stack: typing.List = None
    thread: "comment.Thread" = None


class Image(BaseModel):
    height: int = None
    type: "ImageType" = None
    url: str = None
    width: int = None


class ImageType(Enum):
    s = "s"
    m = "m"
    x = "x"
    o = "o"
    p = "p"
    q = "q"
    r = "r"
    y = "y"
    z = "z"
    w = "w"
    i = "i"
    d = "d"


class MarketAlbumUploadResponse(BaseModel):
    gid: int = None
    hash: str = None
    photo: str = None
    server: int = None


class MarketUploadResponse(BaseModel):
    crop_data: str = None
    crop_hash: str = None
    group_id: int = None
    hash: str = None
    photo: str = None
    server: int = None


class MessageUploadResponse(BaseModel):
    hash: str = None
    photo: str = None
    server: int = None


class OwnerUploadResponse(BaseModel):
    hash: str = None
    photo: str = None
    server: int = None


class Photo(BaseModel):
    access_key: str = None
    album_id: int = None
    date: int = None
    height: int = None
    id: int = None
    images: typing.List[Image] = None
    lat: float = None
    long: float = None
    owner_id: int = None
    post_id: int = None
    sizes: typing.List["PhotoSizes"] = None
    text: str = None
    user_id: int = None
    width: int = None


class PhotoAlbum(BaseModel):
    created: int = None
    description: str = None
    id: int = None
    owner_id: int = None
    size: int = None
    thumb: "Photo" = None
    title: str = None
    updated: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class PhotoAlbumFull(BaseModel):
    can_upload: "base.BoolInt" = None
    comments_disabled: "base.BoolInt" = None
    created: int = None
    description: str = None
    id: int = None
    owner_id: int = None
    size: int = None
    sizes: typing.List["PhotoSizes"] = None
    thumb_id: int = None
    thumb_is_last: "base.BoolInt" = None
    thumb_src: str = None
    title: str = None
    updated: int = None
    upload_by_admins_only: "base.BoolInt" = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class PhotoFull(BaseModel):
    access_key: str = None
    album_id: int = None
    can_comment: "base.BoolInt" = None
    comments: "base.ObjectCount" = None
    date: int = None
    height: int = None
    id: int = None
    images: typing.List[Image] = None
    lat: float = None
    likes: "base.Likes" = None
    long: float = None
    owner_id: int = None
    post_id: int = None
    reposts: "base.ObjectCount" = None
    tags: "base.ObjectCount" = None
    text: str = None
    user_id: int = None
    width: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class PhotoFullXtrRealOffset(BaseModel):
    access_key: str = None
    album_id: int = None
    can_comment: "base.BoolInt" = None
    comments: "base.ObjectCount" = None
    date: int = None
    height: int = None
    hidden: "base.PropertyExists" = None
    id: int = None
    lat: float = None
    likes: "base.Likes" = None
    long: float = None
    owner_id: int = None
    photo_1280: str = None
    photo_130: str = None
    photo_2560: str = None
    photo_604: str = None
    photo_75: str = None
    photo_807: str = None
    post_id: int = None
    real_offset: int = None
    reposts: "base.ObjectCount" = None
    sizes: typing.List["PhotoSizes"] = None
    tags: "base.ObjectCount" = None
    text: str = None
    user_id: int = None
    width: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class PhotoSizes(BaseModel):
    height: int = None
    url: str = None
    src: str = None
    type: "PhotoSizesType" = None
    width: int = None


PhotoSizesType = str


class PhotoTag(BaseModel):
    date: int = None
    id: int = None
    placer_id: int = None
    tagged_name: str = None
    user_id: int = None
    viewed: "base.BoolInt" = None
    x: float = None
    x2: float = None
    y: float = None
    y2: float = None


class PhotoUpload(BaseModel):
    album_id: int = None
    upload_url: str = None
    user_id: int = None


class PhotoUploadResponse(BaseModel):
    aid: int = None
    hash: str = None
    photos_list: str = None
    server: int = None


class PhotoXtrRealOffset(BaseModel):
    access_key: str = None
    album_id: int = None
    date: int = None
    height: int = None
    hidden: "base.PropertyExists" = None
    id: int = None
    lat: float = None
    long: float = None
    owner_id: int = None
    photo_1280: str = None
    photo_130: str = None
    photo_2560: str = None
    photo_604: str = None
    photo_75: str = None
    photo_807: str = None
    post_id: int = None
    real_offset: int = None
    sizes: typing.List["PhotoSizes"] = None
    text: str = None
    user_id: int = None
    width: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class PhotoXtrTagInfo(BaseModel):
    access_key: str = None
    album_id: int = None
    date: int = None
    height: int = None
    id: int = None
    lat: float = None
    long: float = None
    owner_id: int = None
    photo_1280: str = None
    photo_130: str = None
    photo_2560: str = None
    photo_604: str = None
    photo_75: str = None
    photo_807: str = None
    placer_id: int = None
    post_id: int = None
    sizes: typing.List["PhotoSizes"] = None
    tag_created: int = None
    tag_id: int = None
    text: str = None
    user_id: int = None
    width: int = None


class WallUploadResponse(BaseModel):
    hash: str = None
    photo: str = None
    server: int = None


CommentXtrPid.update_forward_refs()
Image.update_forward_refs()
MarketAlbumUploadResponse.update_forward_refs()
MarketUploadResponse.update_forward_refs()
MessageUploadResponse.update_forward_refs()
OwnerUploadResponse.update_forward_refs()
Photo.update_forward_refs()
PhotoAlbum.update_forward_refs()
PhotoAlbumFull.update_forward_refs()
PhotoFull.update_forward_refs()
PhotoFullXtrRealOffset.update_forward_refs()
PhotoSizes.update_forward_refs()
PhotoTag.update_forward_refs()
PhotoUpload.update_forward_refs()
PhotoUploadResponse.update_forward_refs()
PhotoXtrRealOffset.update_forward_refs()
PhotoXtrTagInfo.update_forward_refs()
WallUploadResponse.update_forward_refs()
