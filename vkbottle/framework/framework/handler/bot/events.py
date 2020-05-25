from vkbottle.types.events.events_objects import (
    PhotoComment,
    VideoComment,
    MessageDeny,
    MessageAllow,
    MessageTypingState,
    PhotoCommentDelete,
    WallReplyNew,
    VideoCommentDelete,
    WallPostNew,
    BoardPostNew,
    WallReplyDelete,
    MarketCommentNew,
    BoardPostDelete,
    GroupLeave,
    MarketCommentDelete,
    GroupJoin,
    PollVoteNew,
    UserBlock,
    UserUnblock,
    GroupChangePhoto,
    GroupOfficersEdit,
    GroupChangeSettings,
)
from vkbottle.types.events.events_list import EventList
from vkbottle.types.message import Message
from vkbottle.types.vkpay import VKPayTransaction, AppPayload
from vkbottle.types.objects.photos import Photo
from vkbottle.types.objects.audio import Audio
from vkbottle.types.objects.video import Video
from vkbottle.framework.framework.rule import EventRule
from ..events import ABCEvents


class BotEvents(ABCEvents):
    def message_reply(self):
        def decorator(func):
            rule = EventRule(EventList.MESSAGE_REPLY)
            rule.create(func, {"data": Message})
            self.rules.append(rule)
            return func

        return decorator

    def message_edit(self):
        def decorator(func):
            rule = EventRule(EventList.MESSAGE_EDIT)
            rule.create(func, {"data": Message})
            self.rules.append(rule)
            return func

        return decorator

    def message_deny(self):
        def decorator(func):
            rule = EventRule(EventList.MESSAGE_DENY)
            rule.create(func, {"data": MessageDeny})
            self.rules.append(rule)
            return func

        return decorator

    def message_allow(self):
        def decorator(func):
            rule = EventRule(EventList.MESSAGE_ALLOW)
            rule.create(func, {"data": MessageAllow})
            self.rules.append(rule)
            return func

        return decorator

    def message_typing_state(self):
        def decorator(func):
            rule = EventRule(EventList.MESSAGE_TYPING_STATE)
            rule.create(func, {"data": MessageTypingState})
            self.rules.append(rule)
            return func

        return decorator

    def photo_new(self):
        def decorator(func):
            rule = EventRule(EventList.PHOTO_NEW)
            rule.create(func, {"data": Photo})
            self.rules.append(rule)
            return func

        return decorator

    def photo_comment_new(self):
        def decorator(func):
            rule = EventRule(EventList.PHOTO_COMMENT_NEW)
            rule.create(func, {"data": PhotoComment})
            self.rules.append(rule)
            return func

        return decorator

    def photo_comment_edit(self):
        def decorator(func):
            rule = EventRule(EventList.PHOTO_COMMENT_EDIT)
            rule.create(func, {"data": PhotoComment})
            self.rules.append(rule)
            return func

        return decorator

    def photo_comment_restore(self):
        def decorator(func):
            rule = EventRule(EventList.PHOTO_COMMENT_RESTORE)
            rule.create(func, {"data": PhotoComment})
            self.rules.append(rule)
            return func

        return decorator

    def photo_comment_delete(self):
        def decorator(func):
            rule = EventRule(EventList.PHOTO_COMMENT_DELETE)
            rule.create(func, {"data": PhotoCommentDelete})
            self.rules.append(rule)
            return func

        return decorator

    def audio_new(self):
        def decorator(func):
            rule = EventRule(EventList.AUDIO_NEW)
            rule.create(func, {"data": Audio})
            self.rules.append(rule)
            return func

        return decorator

    def video_new(self):
        def decorator(func):
            rule = EventRule(EventList.VIDEO_NEW)
            rule.create(func, {"data": Video})
            self.rules.append(rule)
            return func

        return decorator

    def video_comment_new(self):
        def decorator(func):
            rule = EventRule(EventList.VIDEO_COMMENT_NEW)
            rule.create(func, {"data": VideoComment})
            self.rules.append(rule)
            return func

        return decorator

    def video_comment_edit(self):
        def decorator(func):
            rule = EventRule(EventList.VIDEO_COMMENT_EDIT)
            rule.create(func, {"data": VideoComment})
            self.rules.append(rule)
            return func

        return decorator

    def video_comment_restore(self):
        def decorator(func):
            rule = EventRule(EventList.VIDEO_COMMENT_RESTORE)
            rule.create(func, {"data": VideoComment})
            self.rules.append(rule)
            return func

        return decorator

    def video_comment_delete(self):
        def decorator(func):
            rule = EventRule(EventList.VIDEO_COMMENT_DELETE)
            rule.create(func, {"data": VideoCommentDelete})
            self.rules.append(rule)
            return func

        return decorator

    def wall_post_new(self):
        def decorator(func):
            rule = EventRule(EventList.WALL_POST_NEW)
            rule.create(func, {"data": WallPostNew})
            self.rules.append(rule)
            return func

        return decorator

    def wall_repost(self):
        def decorator(func):
            rule = EventRule(EventList.WALL_REPOST)
            rule.create(func, {"data": WallPostNew})
            self.rules.append(rule)
            return func

        return decorator

    def wall_reply_new(self):
        def decorator(func):
            rule = EventRule(EventList.WALL_REPLY_NEW)
            rule.create(func, {"data": WallReplyNew})
            self.rules.append(rule)
            return func

        return decorator

    def wall_reply_edit(self):
        def decorator(func):
            rule = EventRule(EventList.WALL_REPLY_EDIT)
            rule.create(func, {"data": WallReplyNew})
            self.rules.append(rule)
            return func

        return decorator

    def wall_reply_restore(self):
        def decorator(func):
            rule = EventRule(EventList.WALL_REPLY_RESTORE)
            rule.create(func, {"data": WallReplyNew})
            self.rules.append(rule)
            return func

        return decorator

    def wall_reply_delete(self):
        def decorator(func):
            rule = EventRule(EventList.WALL_REPLY_DELETE)
            rule.create(func, {"data": WallReplyDelete})
            self.rules.append(rule)
            return func

        return decorator

    def board_post_new(self):
        def decorator(func):
            rule = EventRule(EventList.BOARD_POST_NEW)
            rule.create(func, {"data": BoardPostNew})
            self.rules.append(rule)
            return func

        return decorator

    def board_post_edit(self):
        def decorator(func):
            rule = EventRule(EventList.BOARD_POST_EDIT)
            rule.create(func, {"data": BoardPostNew})
            self.rules.append(rule)
            return func

        return decorator

    def board_post_restore(self):
        def decorator(func):
            rule = EventRule(EventList.BOARD_POST_RESTORE)
            rule.create(func, {"data": BoardPostNew})
            self.rules.append(rule)
            return func

        return decorator

    def board_post_delete(self):
        def decorator(func):
            rule = EventRule(EventList.BOARD_POST_DELETE)
            rule.create(func, {"data": BoardPostDelete})
            self.rules.append(rule)
            return func

        return decorator

    def market_comment_new(self):
        def decorator(func):
            rule = EventRule(EventList.MARKET_COMMENT_NEW)
            rule.create(func, {"data": MarketCommentNew})
            self.rules.append(rule)
            return func

        return decorator

    def market_comment_edit(self):
        def decorator(func):
            rule = EventRule(EventList.MARKET_COMMENT_EDIT)
            rule.create(func, {"data": MarketCommentNew})
            self.rules.append(rule)
            return func

        return decorator

    def market_comment_restore(self):
        def decorator(func):
            rule = EventRule(EventList.MARKET_COMMENT_RESTORE)
            rule.create(func, {"data": MarketCommentNew})
            self.rules.append(rule)
            return func

        return decorator

    def market_comment_delete(self):
        def decorator(func):
            rule = EventRule(EventList.MARKET_COMMENT_DELETE)
            rule.create(func, {"data": MarketCommentDelete})
            self.rules.append(rule)
            return func

        return decorator

    def group_join(self):
        def decorator(func):
            rule = EventRule(EventList.GROUP_JOIN)
            rule.create(func, {"data": GroupJoin})
            self.rules.append(rule)
            return func

        return decorator

    def group_leave(self):
        def decorator(func):
            rule = EventRule(EventList.GROUP_LEAVE)
            rule.create(func, {"data": GroupLeave})
            self.rules.append(rule)
            return func

        return decorator

    def user_block(self):
        def decorator(func):
            rule = EventRule(EventList.USER_BLOCK)
            rule.create(func, {"data": UserBlock})
            self.rules.append(rule)
            return func

        return decorator

    def user_unblock(self):
        def decorator(func):
            rule = EventRule(EventList.USER_UNBLOCK)
            rule.create(func, {"data": UserUnblock})
            self.rules.append(rule)
            return func

        return decorator

    def poll_vote_new(self):
        def decorator(func):
            rule = EventRule(EventList.POLL_VOTE_NEW)
            rule.create(func, {"data": PollVoteNew})
            self.rules.append(rule)
            return func

        return decorator

    def group_officers_edit(self):
        def decorator(func):
            rule = EventRule(EventList.GROUP_OFFICERS_EDIT)
            rule.create(func, {"data": GroupOfficersEdit})
            self.rules.append(rule)
            return func

        return decorator

    def group_change_settings(self):
        def decorator(func):
            rule = EventRule(EventList.GROUP_CHANGE_SETTINGS)
            rule.create(func, {"data": GroupChangeSettings})
            self.rules.append(rule)
            return func

        return decorator

    def group_change_photo(self):
        def decorator(func):
            rule = EventRule(EventList.GROUP_CHANGE_PHOTO)
            rule.create(func, {"data": GroupChangePhoto})
            self.rules.append(rule)
            return func

        return decorator

    def vkpay_transaction(self):
        def decorator(func):
            rule = EventRule(EventList.VKPAY_TRANSACTION)
            rule.create(func, {"data": VKPayTransaction})
            self.rules.append(rule)
            return func

        return decorator

    def app_payload(self):
        def decorator(func):
            rule = EventRule(EventList.APP_PAYLOAD)
            rule.create(func, {"data": AppPayload})
            self.rules.append(rule)
            return func

        return decorator
