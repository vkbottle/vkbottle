from enum import Enum
from ...base import BaseModel
from .events_list import Event as events
from . import events_objects as EventsObjects

from ...message import Message
from ...attachments import Photo, Audio, Video

from ...wall_post import WallPost

import pydantic

# https://vk.com/dev/groups_events


class BaseEvent(BaseModel):
    group_id: int = None
    type: Enum = None


class MessageNew(BaseEvent):
    type: str = None
    object: Message = None


class MessageReply(MessageNew):
    type: str = None


class MessageAllow(BaseEvent):
    type: str = None
    object: EventsObjects.MessageAllow = None


class MessageDeny(BaseEvent):
    type: str = None
    object: EventsObjects.MessageAllow = None


class PhotoNew(BaseEvent):
    type: str = None
    object: Photo = None


class PhotoCommentNew(BaseEvent):
    type: str = None
    object: EventsObjects.PhotoCommentNew = None


class PhotoCommentEdit(PhotoCommentNew):
    type: str = None


class PhotoCommentRestore(PhotoCommentNew):
    type: str = None


class PhotoCommentDelete(BaseEvent):
    type: str = None
    object: EventsObjects.PhotoCommentDelete = None


class AudioNew(BaseEvent):
    type: str = None
    object: Audio = None


class VideoNew(BaseEvent):
    type: str = None
    object: Video = None


class VideoCommentNew(BaseEvent):
    type: str = None
    object: EventsObjects.VideoCommentNew = None


class VideoCommentEdit(VideoCommentNew):
    type: str = None


class VideoCommentRestore(VideoCommentNew):
    type: str = None


class VideoCommentDelete(BaseEvent):
    type: str = None
    object: EventsObjects.VideoCommentDelete = None


class WallPostNew(BaseEvent):
    type: str = None
    object: WallPost = None


class WallRepost(WallPostNew):
    type: str = None


class WallReplyNew(BaseEvent):
    type: str = None
    object: EventsObjects.WallReplyNew = None


class WallReplyEdit(WallReplyNew):
    type: str = None


class WallReplyRestore(WallReplyNew):
    type: str = None


class WallReplyDelete(BaseEvent):
    type: str = None
    object: EventsObjects.WallReplyDelete = None


class BoardPostNew(BaseEvent):
    type: str = None
    object: EventsObjects.BoardPostNew = None


class BoardPostEdit(BoardPostNew):
    type: str = None


class BoardPostRestore(BoardPostNew):
    type: str = None


class BoardPostDelete(BaseEvent):
    type: str = None
    object: EventsObjects.BoardPostDelete = None


class MarketCommentNew(BaseEvent):
    type: str = None
    object: EventsObjects.MarketCommentNew = None


class MarketCommentEdit(MarketCommentNew):
    type: str = None


class MarketCommentRestore(MarketCommentNew):
    type: str = None


class MarketCommentDelete(BaseEvent):
    type: str = None
    object: EventsObjects.MarketCommentDelete = None


class GroupLeave(BaseEvent):
    type: str = None
    object: EventsObjects.GroupLeave = None


class GroupJoin(BaseEvent):
    type: str = None
    object: EventsObjects.GroupJoin = None


class UserBlock(BaseEvent):
    type: str = None
    object: EventsObjects.UserBlock = None


class UserUnblock(BaseEvent):
    type: str = None
    object: EventsObjects.UserUnblock = None


class PollVoteNew(BaseEvent):
    type: str = None
    object: EventsObjects.PollVoteNew = None


class GroupOfficersEdit(BaseEvent):
    type: str = None
    object: EventsObjects.GroupOfficersEdit = None


class GroupChangeSettings(BaseEvent):
    type: str = None
    object: EventsObjects.GroupChangeSettings = None


class GroupChangePhoto(BaseEvent):
    type: str = None
    object: EventsObjects.GroupChangePhoto = None


Audio.update_forward_refs()
AudioNew.update_forward_refs()
BaseEvent.update_forward_refs()
BaseModel.update_forward_refs()
BoardPostDelete.update_forward_refs()
BoardPostEdit.update_forward_refs()
BoardPostNew.update_forward_refs()
BoardPostRestore.update_forward_refs()
GroupChangePhoto.update_forward_refs()
GroupChangeSettings.update_forward_refs()
GroupJoin.update_forward_refs()
GroupLeave.update_forward_refs()
GroupOfficersEdit.update_forward_refs()
MarketCommentDelete.update_forward_refs()
MarketCommentEdit.update_forward_refs()
MarketCommentNew.update_forward_refs()
MarketCommentRestore.update_forward_refs()
Message.update_forward_refs()
MessageAllow.update_forward_refs()
MessageDeny.update_forward_refs()
MessageNew.update_forward_refs()
MessageReply.update_forward_refs()
Photo.update_forward_refs()
PhotoCommentDelete.update_forward_refs()
PhotoCommentEdit.update_forward_refs()
PhotoCommentNew.update_forward_refs()
PhotoCommentRestore.update_forward_refs()
PhotoNew.update_forward_refs()
PollVoteNew.update_forward_refs()
UserBlock.update_forward_refs()
UserUnblock.update_forward_refs()
Video.update_forward_refs()
VideoCommentDelete.update_forward_refs()
VideoCommentEdit.update_forward_refs()
VideoCommentNew.update_forward_refs()
VideoCommentRestore.update_forward_refs()
VideoNew.update_forward_refs()
WallPost.update_forward_refs()
WallPostNew.update_forward_refs()
WallReplyDelete.update_forward_refs()
WallReplyEdit.update_forward_refs()
WallReplyNew.update_forward_refs()
WallReplyRestore.update_forward_refs()
WallRepost.update_forward_refs()
