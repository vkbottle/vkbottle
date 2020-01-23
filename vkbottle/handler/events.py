from ..types.events.community.events_objects import *
from ..types.events.community.events_list import EventList
from ..types.message import Message
from ..types.vkpay import VKPayTransaction, AppPayload
from ..types.attachments.photo import Photo
from ..types.attachments.audio import Audio
from ..types.attachments.video import Video
import typing
from ..framework.rule import EventRule


class Event(object):
    def __init__(self):
        self.rules: typing.List[EventRule] = list()

    def __call__(self, *events):
        def decorator(func):
            rule = EventRule(list(events))
            rule.create(func)
            self.rules.append(rule)
            return func

        return decorator

    def rule(self, rule):
        def decorator(func):
            rule.create(func)
            self.rules.append(rule)
            return func

        return decorator

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
            self.events[EventList.GROUP_LEAVE] = {"call": func, "data": GroupLeave}
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
