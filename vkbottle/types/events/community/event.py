from enum import Enum
from typing import Union
from ...base import BaseModel
from .events_list import EventList as events
from . import events_objects as EventsObjects

from ...message import Message
from ...attachments import Photo, Audio, Video

from ...wall_post import WallPost


# https://vk.com/dev/groups_events


EVENT_DICT = {}


class SetEventDict:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        if self.name not in EVENT_DICT:
            EVENT_DICT[self.name] = cls
        return cls


class BaseEvent(BaseModel):
    group_id: int = None
    type: Union[Enum, str] = None


@SetEventDict(events.MESSAGE_NEW)
class MessageNew(BaseEvent):
    object: Message = None


@SetEventDict(events.MESSAGE_EDIT)
class MessageEdit(MessageNew):
    ...


@SetEventDict(events.MESSAGE_REPLY)
class MessageReply(MessageNew):
    ...


@SetEventDict(events.MESSAGE_ALLOW)
class MessageAllow(BaseEvent):
    object: EventsObjects.MessageAllow = None


@SetEventDict(events.MESSAGE_DENY)
class MessageDeny(BaseEvent):
    object: EventsObjects.MessageAllow = None


@SetEventDict(events.PHOTO_NEW)
class PhotoNew(BaseEvent):
    object: Photo = None


@SetEventDict(events.PHOTO_COMMENT_NEW)
class PhotoCommentNew(BaseEvent):
    object: EventsObjects.PhotoComment = None


@SetEventDict(events.PHOTO_COMMENT_EDIT)
class PhotoCommentEdit(PhotoCommentNew):
    ...


@SetEventDict(events.PHOTO_COMMENT_RESTORE)
class PhotoCommentRestore(PhotoCommentNew):
    ...


@SetEventDict(events.PHOTO_COMMENT_DELETE)
class PhotoCommentDelete(BaseEvent):
    object: EventsObjects.PhotoCommentDelete = None


@SetEventDict(events.AUDIO_NEW)
class AudioNew(BaseEvent):
    object: Audio = None


@SetEventDict(events.VIDEO_NEW)
class VideoNew(BaseEvent):
    object: Video = None


@SetEventDict(events.VIDEO_COMMENT_NEW)
class VideoCommentNew(BaseEvent):
    object: EventsObjects.VideoComment = None


@SetEventDict(events.VIDEO_COMMENT_EDIT)
class VideoCommentEdit(VideoCommentNew):
    ...


@SetEventDict(events.VIDEO_COMMENT_RESTORE)
class VideoCommentRestore(VideoCommentNew):
    ...


@SetEventDict(events.VIDEO_COMMENT_DELETE)
class VideoCommentDelete(BaseEvent):
    object: EventsObjects.VideoCommentDelete = None


@SetEventDict(events.WALL_POST_NEW)
class WallPostNew(BaseEvent):
    object: WallPost = None


@SetEventDict(events.WALL_REPOST)
class WallRepost(WallPostNew):
    ...


@SetEventDict(events.WALL_REPLY_NEW)
class WallReplyNew(BaseEvent):
    object: EventsObjects.WallReplyNew = None


@SetEventDict(events.WALL_REPLY_EDIT)
class WallReplyEdit(WallReplyNew):
    ...


@SetEventDict(events.WALL_REPLY_RESTORE)
class WallReplyRestore(WallReplyNew):
    ...


@SetEventDict(events.WALL_REPLY_DELETE)
class WallReplyDelete(BaseEvent):
    object: EventsObjects.WallReplyDelete = None


@SetEventDict(events.BOARD_POST_NEW)
class BoardPostNew(BaseEvent):
    object: EventsObjects.BoardPostNew = None


@SetEventDict(events.BOARD_POST_EDIT)
class BoardPostEdit(BoardPostNew):
    ...


@SetEventDict(events.BOARD_POST_RESTORE)
class BoardPostRestore(BoardPostNew):
    ...


@SetEventDict(events.BOARD_POST_DELETE)
class BoardPostDelete(BaseEvent):
    object: EventsObjects.BoardPostDelete = None


@SetEventDict(events.MARKET_COMMENT_NEW)
class MarketCommentNew(BaseEvent):
    object: EventsObjects.MarketCommentNew = None


@SetEventDict(events.MARKET_COMMENT_EDIT)
class MarketCommentEdit(MarketCommentNew):
    ...


@SetEventDict(events.MARKET_COMMENT_RESTORE)
class MarketCommentRestore(MarketCommentNew):
    ...


@SetEventDict(events.MARKET_COMMENT_DELETE)
class MarketCommentDelete(BaseEvent):
    object: EventsObjects.MarketCommentDelete = None


@SetEventDict(events.GROUP_LEAVE)
class GroupLeave(BaseEvent):
    object: EventsObjects.GroupLeave = None


@SetEventDict(events.GROUP_JOIN)
class GroupJoin(BaseEvent):
    object: EventsObjects.GroupJoin = None


@SetEventDict(events.USER_BLOCK)
class UserBlock(BaseEvent):
    object: EventsObjects.UserBlock = None


@SetEventDict(events.USER_UNBLOCK)
class UserUnblock(BaseEvent):
    object: EventsObjects.UserUnblock = None


@SetEventDict(events.POLL_VOTE_NEW)
class PollVoteNew(BaseEvent):
    object: EventsObjects.PollVoteNew = None


@SetEventDict(events.GROUP_OFFICERS_EDIT)
class GroupOfficersEdit(BaseEvent):
    object: EventsObjects.GroupOfficersEdit = None


@SetEventDict(events.GROUP_CHANGE_SETTINGS)
class GroupChangeSettings(BaseEvent):
    object: EventsObjects.GroupChangeSettings = None


@SetEventDict(events.GROUP_CHANGE_PHOTO)
class GroupChangePhoto(BaseEvent):
    object: EventsObjects.GroupChangePhoto = None
