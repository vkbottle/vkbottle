from vkbottle.types.base import BaseModel

from vkbottle.types.objects.wall import WallComment
from vkbottle.types.objects.wall import Wallpost
from vkbottle.types.objects.board import TopicComment
from vkbottle.types.objects.photos import Photo

from typing import Any
from enum import Enum, IntEnum


class BlockReason(IntEnum):
    other = 0
    spam = 1
    verbal_abuse = 2
    strong_language = 3
    irrelevant_messages = 4


class JoinType(Enum):
    join = "join"
    unsure = "unsure"
    accepted = "accepted"
    approved = "approved"
    request = "request"


class AdminLevel(IntEnum):
    no_role = 0
    moderator = 1
    editor = 2
    administrator = 3


class MessageAllow(BaseModel):
    user_id: int = None
    key: str = None
    api: list = None


class MessageTypingState(BaseModel):
    state: str = None
    from_id: int = None
    to_id: int = None
    api: list = None


class MessageDeny(BaseModel):
    user_id: int = None


class PhotoComment(WallComment):
    photo_id: int = None
    photo_owner_id: int = None


class PhotoCommentDelete(BaseModel):
    owner_id: int = None
    id: int = None
    user_id: int = None
    photo_id: int = None


class VideoComment(WallComment):
    video_id: int = None
    video_owner_id: int = None


class VideoCommentDelete(BaseModel):
    owner_id: int = None
    id: int = None
    user_id: int = None
    video_id: int = None


class WallPostNew(Wallpost):
    postponed_id: int = None


class WallReplyNew(WallComment):
    post_id: int = None
    post_owner_id: int = None
    api: list = None

    async def answer(self, message: str = None, **params):
        await self.api[0].wall.createComment(
            message=message,
            reply_to_comment=self.id,
            from_group=self.api[0].group_id,
            owner_id=-self.api[0].group_id,
            post_id=self.post_id,
            **params
        )


class WallReplyDelete(BaseModel):
    owner_id: int = None
    id: int = None
    user_id: int = None
    deleter_id: int = None
    post_id: int = None


class BoardPostNew(TopicComment):
    topic_id: int = None
    topic_owner_id: int = None


class BoardPostDelete(BaseModel):
    topic_id: int = None
    id: int = None


class MarketCommentNew(WallComment):
    market_owner_id: int = None
    item_id: int = None


class MarketCommentDelete(BaseModel):
    owner_id: int = None
    id: int = None
    user_id: int = None
    item_id: int = None


class GroupLeave(BaseModel):
    user_id: int = None
    self: int = None


class GroupJoin(BaseModel):
    user_id: int = None
    join_type: JoinType = None


class UserBlock(BaseModel):
    admin_id: int = None
    user_id: int = None
    unblock_data: int = None
    reason: BlockReason = None
    comment: str = None


class UserUnblock(BaseModel):
    admin_id: int = None
    user_id: int = None
    by_end_date: int = None


class PollVoteNew(BaseModel):
    owner_id: int = None
    poll_id: int = None
    option_id: int = None
    user_id: int = None


class GroupOfficersEdit(BaseModel):
    admin_id: int = None
    user_id: int = None
    level_old: AdminLevel = None
    level_new: AdminLevel = None


class GroupChangeSettingsChangesSectionEnable(Enum):
    status_default = "status_default"
    audio = "audio"
    photo = "photo"
    video = "video"
    market = "market"


class GroupChangeSettingsChangesSectionName(Enum):
    title = "title"
    description = "description"
    community_type = "access"
    screen_name = "screen_name"
    public_category = "public_category"
    public_subcategory = "public_subcategory"
    age_limits = "age_limits"
    website = "website"
    enable_section = GroupChangeSettingsChangesSectionEnable


class GroupChangeSettingsChanges(BaseModel):
    section_name: GroupChangeSettingsChangesSectionName = None
    old_value: Any = None
    new_value: Any = None


class GroupChangeSettings(BaseModel):
    user_id: int = None
    changes: GroupChangeSettingsChanges = None


class GroupChangePhoto(BaseModel):
    user_id: int = None
    photo: Photo = None
