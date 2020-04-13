from . import base, messages, wall
import typing
from enum import Enum
from ..base import BaseModel


class AccountCounters(BaseModel):
    app_requests: int = None
    events: int = None
    friends: int = None
    friends_suggestions: int = None
    gifts: int = None
    groups: int = None
    messages: int = None
    notifications: int = None
    photos: int = None
    videos: int = None


class Info(BaseModel):
    _2fa_required: "base.BoolInt" = None
    country: str = None
    https_required: "base.BoolInt" = None
    intro: "base.BoolInt" = None
    lang: int = None
    no_wall_replies: "base.BoolInt" = None
    own_posts_default: "base.BoolInt" = None


class NameRequest(BaseModel):
    first_name: str = None
    id: int = None
    last_name: str = None
    status: "NameRequestStatus" = None
    lang: str = None


class NameRequestStatus(Enum):
    success = "success"
    processing = "processing"
    declined = "declined"
    was_accepted = "was_accepted"
    was_declined = "was_declined"


class Offer(BaseModel):
    description: str = None
    id: int = None
    img: str = None
    instruction: str = None
    instruction_html: str = None
    price: int = None
    short_description: str = None
    tag: str = None
    title: str = None


class PushConversations(BaseModel):
    count: int = None
    items: typing.List["PushConversationsItem"] = None


class PushConversationsItem(BaseModel):
    disabled_until: int = None
    peer_id: int = None
    sound: "base.BoolInt" = None


class PushParams(BaseModel):
    msg: typing.List["PushParamsMode"] = None
    chat: typing.List["PushParamsMode"] = None
    like: typing.List[base.Likes] = None
    repost: typing.List[base.RepostsInfo] = None
    comment: typing.List[base.CommentsInfo] = None
    mention: typing.List["PushParamsMutual"] = None
    reply: typing.List[messages.Message] = None
    new_post: typing.List[wall.Wallpost] = None
    wall_post: typing.List[wall.Wallpost] = None
    wall_publish: typing.List[wall.Wallpost] = None
    friend: typing.List["PushParamsMutual"] = None
    friend_found: typing.List["PushParamsMutual"] = None
    friend_accepted: typing.List[dict] = None
    group_invite: typing.List[dict] = None
    group_accepted: typing.List[dict] = None
    birthday: typing.List[dict] = None
    event_soon: typing.List[dict] = None
    app_request: typing.List[dict] = None
    sdk_open: typing.List[dict] = None


class PushParamsMode(Enum):
    on = "on"
    off = "off"
    no_sound = "no_sound"
    no_text = "no_text"


class PushParamsMutual(Enum):
    mutual = "mutual"


class PushParamsOnoff(Enum):
    on = "on"
    off = "off"


class PushParamsSettings(Enum):
    on = "on"
    off = "off"
    fr_of_fr = "fr_of_fr"


class PushSettings(BaseModel):
    disabled: "base.BoolInt" = None
    disabled_until: int = None
    settings: "PushParams" = None
    conversations: "PushConversations" = None


class UserSettingsInterest(BaseModel):
    title: str = None
    value: str = None


class UserSettingsInterests(BaseModel):
    activities: "UserSettingsInterest" = None
    interests: "UserSettingsInterest" = None
    music: "UserSettingsInterest" = None
    tv: "UserSettingsInterest" = None
    movies: "UserSettingsInterest" = None
    books: "UserSettingsInterest" = None
    games: "UserSettingsInterest" = None
    quotes: "UserSettingsInterest" = None
    about: "UserSettingsInterest" = None


AccountCounters.update_forward_refs()
Info.update_forward_refs()
NameRequest.update_forward_refs()
Offer.update_forward_refs()
PushConversations.update_forward_refs()
PushConversationsItem.update_forward_refs()
PushParams.update_forward_refs()
PushSettings.update_forward_refs()
UserSettingsInterest.update_forward_refs()
UserSettingsInterests.update_forward_refs()
