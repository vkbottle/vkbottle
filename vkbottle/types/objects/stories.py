from . import base, photos, video
from enum import Enum
from ..base import BaseModel


class PromoBlock(BaseModel):
    name: str = None
    photo_50: str = None
    photo_100: str = None
    not_animated: bool = None


class Replies(BaseModel):
    count: int = None
    new: int = None


class Story(BaseModel):
    access_key: str = None
    can_comment: "base.BoolInt" = None
    can_reply: "base.BoolInt" = None
    can_see: "base.BoolInt" = None
    can_share: "base.BoolInt" = None
    date: int = None
    expires_at: int = None
    id: int = None
    is_deleted: bool = None
    is_expired: bool = None
    link: "StoryLink" = None
    owner_id: int = None
    parent_story: "Story" = None
    parent_story_access_key: str = None
    parent_story_id: int = None
    parent_story_owner_id: int = None
    photo: "photos.Photo" = None
    replies: "Replies" = None
    seen: "base.BoolInt" = None
    type: "StoryType" = None
    video: "StoryVideo" = None
    views: int = None
    is_restricted: bool = None
    no_sound: bool = None
    need_mute: bool = None
    can_ask: "base.BoolInt" = None
    can_ask_anonymous: "base.BoolInt" = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class StoryLink(BaseModel):
    text: str = None
    url: str = None


class StoryStats(BaseModel):
    answer: "StoryStatsStat" = None
    bans: "StoryStatsStat" = None
    open_link: "StoryStatsStat" = None
    replies: "StoryStatsStat" = None
    shares: "StoryStatsStat" = None
    subscribers: "StoryStatsStat" = None
    views: "StoryStatsStat" = None


class StoryStatsStat(BaseModel):
    count: int = None
    state: "StoryStatsState" = None


class StoryStatsState(Enum):
    on = "on"
    off = "off"
    hidden = "hidden"


class StoryType(Enum):
    photo = "photo"
    video = "video"


class StoryVideo(video.Video):
    is_private: "base.BoolInt" = None


class UploadLinkText(Enum):
    to_store = "to_store"
    vote = "vote"
    more = "more"
    book = "book"
    order = "order"
    enroll = "enroll"
    fill = "fill"
    signup = "signup"
    buy = "buy"
    ticket = "ticket"
    write = "write"
    open = "open"
    learn_more = "learn_more"
    view = "view"
    go_to = "go_to"
    contact = "contact"
    watch = "watch"
    play = "play"
    install = "install"
    read = "read"


PromoBlock.update_forward_refs()
Replies.update_forward_refs()
Story.update_forward_refs()
StoryLink.update_forward_refs()
StoryStats.update_forward_refs()
StoryStatsStat.update_forward_refs()
StoryVideo.update_forward_refs()
