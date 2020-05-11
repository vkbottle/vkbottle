from . import photos, base, groups
import typing
from enum import Enum
from ..base import BaseModel


class BoardPostDelete(BaseModel):
    topic_owner_id: int = None
    topic_id: int = None
    id: int = None


class ConfirmationMessage(BaseModel):
    type: "MessageType" = None
    group_id: int = None
    secret: str = None


class GroupChangePhoto(BaseModel):
    user_id: int = None
    photo: "photos.Photo" = None


class GroupChangeSettings(BaseModel):
    user_id: int = None
    self: "base.BoolInt" = None


class GroupJoin(BaseModel):
    user_id: int = None
    join_type: "GroupJoinType" = None


class GroupJoinType(Enum):
    join = "join"
    unsure = "unsure"
    accepted = "accepted"
    approved = "approved"
    request = "request"


class GroupLeave(BaseModel):
    user_id: int = None
    self: "base.BoolInt" = None


class GroupOfficersEdit(BaseModel):
    admin_id: int = None
    user_id: int = None
    level_old: int = None
    level_new: int = None


class GroupSettingsChanges(BaseModel):
    title: str = None
    description: str = None
    access: int = None
    screen_name: str = None
    public_category: int = None
    public_subcategory: int = None
    age_limits: int = None
    website: str = None
    enable_status_default: int = None
    enable_audio: int = None
    enable_video: int = None
    enable_photo: int = None
    enable_market: int = None


class MarketComment(BaseModel):
    id: int = None
    from_id: int = None
    date: int = None
    text: str = None
    market_owner_od: int = None
    photo_id: int = None


class MarketCommentDelete(BaseModel):
    owner_id: int = None
    id: int = None
    user_id: int = None
    item_id: int = None


class MessageAllow(BaseModel):
    user_id: int = None
    key: str = None


class MessageBase(BaseModel):
    type: "MessageType" = None
    object: typing.Dict = None
    group_id: int = None


class MessageDeny(BaseModel):
    user_id: int = None


class MessageType(Enum):
    confirmation = "confirmation"
    group_change_photo = "group_change_photo"
    group_change_settings = "group_change_settings"
    group_officers_edit = "group_officers_edit"
    lead_forms_new = "lead_forms_new"
    market_comment_delete = "market_comment_delete"
    market_comment_edit = "market_comment_edit"
    market_comment_restore = "market_comment_restore"
    message_allow = "message_allow"
    message_deny = "message_deny"
    message_read = "message_read"
    message_reply = "message_reply"
    message_typing_state = "message_typing_state"
    messages_edit = "messages_edit"
    photo_comment_delete = "photo_comment_delete"
    photo_comment_edit = "photo_comment_edit"
    photo_comment_restore = "photo_comment_restore"
    poll_vote_new = "poll_vote_new"
    user_block = "user_block"
    user_unblock = "user_unblock"
    video_comment_delete = "video_comment_delete"
    video_comment_edit = "video_comment_edit"
    video_comment_restore = "video_comment_restore"
    wall_reply_delete = "wall_reply_delete"
    wall_reply_restore = "wall_reply_restore"
    wall_repost = "wall_repost"


class PhotoComment(BaseModel):
    id: int = None
    from_id: int = None
    date: int = None
    text: str = None
    photo_owner_od: int = None


class PhotoCommentDelete(BaseModel):
    id: int = None
    owner_id: int = None
    user_id: int = None
    photo_id: int = None


class PollVoteNew(BaseModel):
    owner_id: int = None
    poll_id: int = None
    option_id: int = None
    user_id: int = None


class UserBlock(BaseModel):
    admin_id: int = None
    user_id: int = None
    unblock_date: int = None
    reason: int = None
    comment: str = None


class UserUnblock(BaseModel):
    admin_id: int = None
    user_id: int = None
    by_end_date: int = None


class VideoComment(BaseModel):
    id: int = None
    from_id: int = None
    date: int = None
    text: str = None
    video_owner_od: int = None


class VideoCommentDelete(BaseModel):
    id: int = None
    owner_id: int = None
    user_id: int = None
    video_id: int = None


class WallCommentDelete(BaseModel):
    owner_id: int = None
    id: int = None
    user_id: int = None
    post_id: int = None


BoardPostDelete.update_forward_refs()
ConfirmationMessage.update_forward_refs()
GroupChangePhoto.update_forward_refs()
GroupChangeSettings.update_forward_refs()
GroupJoin.update_forward_refs()
GroupLeave.update_forward_refs()
GroupOfficersEdit.update_forward_refs()
GroupSettingsChanges.update_forward_refs()
MarketComment.update_forward_refs()
MarketCommentDelete.update_forward_refs()
MessageAllow.update_forward_refs()
MessageBase.update_forward_refs()
MessageDeny.update_forward_refs()
PhotoComment.update_forward_refs()
PhotoCommentDelete.update_forward_refs()
PollVoteNew.update_forward_refs()
UserBlock.update_forward_refs()
UserUnblock.update_forward_refs()
VideoComment.update_forward_refs()
VideoCommentDelete.update_forward_refs()
WallCommentDelete.update_forward_refs()
