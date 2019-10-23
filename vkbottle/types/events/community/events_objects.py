from ...base import BaseModel

from ...wall_comment import WallComment
from ...wall_post import WallPost
from ...attachments.topic import TopicComment

from ...additional import JoinType, BlockReason, AdminLevel
from ...attachments import Photo

import typing
import random

from enum import Enum


class MessageAllow(BaseModel):
    user_id: int = None
    key: typing.Optional[str] = None
    api: list = None

    async def __call__(
        self,
        message: str = None,
        attachment: str = None,
        keyboard: dict = None,
        **params
    ):
        return await self.api[0].request(
            "messages",
            "send",
            dict(
                message=message,
                peer_id=self.user_id,
                attachment=attachment,
                keyboard=keyboard,
                random_id=random.randint(-2e9, 2e9),
                **params
            ),
        )


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


class WallPostNew(WallPost):
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
    old_value: typing.Any = None
    new_value: typing.Any = None


class GroupChangeSettings(BaseModel):
    user_id: int = None
    changes: GroupChangeSettingsChanges = None


class GroupChangePhoto(BaseModel):
    user_id: int = None
    photo: Photo = None
