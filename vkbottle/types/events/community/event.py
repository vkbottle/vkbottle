from enum import Enum
from typing import Union
from ...base import BaseModel
from .events_list import EventList as events
from . import events_objects as EventsObjects

from ...message import Message
from ...attachments import Photo, Audio, Video

from ...wall_post import WallPost


# https://vk.com/dev/groups_events


class BaseEvent(BaseModel):
    group_id: int = None
    type: Union[Enum, str] = None


class MessageNew(BaseEvent):
    object: Message = None


class MessageReply(MessageNew):
    ...


class MessageAllow(BaseEvent):
    object: EventsObjects.MessageAllow = None


class MessageDeny(BaseEvent):
    object: EventsObjects.MessageAllow = None


class PhotoNew(BaseEvent):
    object: Photo = None


class PhotoCommentNew(BaseEvent):
    object: EventsObjects.PhotoComment = None


class PhotoCommentEdit(PhotoCommentNew):
    ...


class PhotoCommentRestore(PhotoCommentNew):
    ...


class PhotoCommentDelete(BaseEvent):
    object: EventsObjects.PhotoCommentDelete = None


class AudioNew(BaseEvent):
    object: Audio = None


class VideoNew(BaseEvent):
    object: Video = None


class VideoCommentNew(BaseEvent):
    object: EventsObjects.VideoComment = None


class VideoCommentEdit(VideoCommentNew):
    ...


class VideoCommentRestore(VideoCommentNew):
    ...


class VideoCommentDelete(BaseEvent):
    object: EventsObjects.VideoCommentDelete = None


class WallPostNew(BaseEvent):
    object: WallPost = None


class WallRepost(WallPostNew):
    ...


class WallReplyNew(BaseEvent):
    object: EventsObjects.WallReplyNew = None


class WallReplyEdit(WallReplyNew):
    ...


class WallReplyRestore(WallReplyNew):
    ...


class WallReplyDelete(BaseEvent):
    object: EventsObjects.WallReplyDelete = None


class BoardPostNew(BaseEvent):
    object: EventsObjects.BoardPostNew = None


class BoardPostEdit(BoardPostNew):
    ...


class BoardPostRestore(BoardPostNew):
    ...


class BoardPostDelete(BaseEvent):
    object: EventsObjects.BoardPostDelete = None


class MarketCommentNew(BaseEvent):
    object: EventsObjects.MarketCommentNew = None


class MarketCommentEdit(MarketCommentNew):
    ...


class MarketCommentRestore(MarketCommentNew):
    ...


class MarketCommentDelete(BaseEvent):
    object: EventsObjects.MarketCommentDelete = None


class GroupLeave(BaseEvent):
    object: EventsObjects.GroupLeave = None


class GroupJoin(BaseEvent):
    object: EventsObjects.GroupJoin = None


class UserBlock(BaseEvent):
    object: EventsObjects.UserBlock = None


class UserUnblock(BaseEvent):
    object: EventsObjects.UserUnblock = None


class PollVoteNew(BaseEvent):
    object: EventsObjects.PollVoteNew = None


class GroupOfficersEdit(BaseEvent):
    object: EventsObjects.GroupOfficersEdit = None


class GroupChangeSettings(BaseEvent):
    object: EventsObjects.GroupChangeSettings = None


class GroupChangePhoto(BaseEvent):
    object: EventsObjects.GroupChangePhoto = None
