from ..types.events.community.events_objects import *
from ..types.events.community.events_list import EventList
from ..types.message import Message
from ..types.attachments.photo import Photo
from ..types.attachments.audio import Audio
from ..types.attachments.video import Video


class Event(object):
    def __init__(self):
        self.events = dict()

    def message_reply(self):
        def decorator(func):
            self.events[EventList.MESSAGE_REPLY] = {"call": func, "data": Message}
            return func

        return decorator

    def message_deny(self):
        def decorator(func):
            self.events[EventList.MESSAGE_DENY] = {"call": func, "data": MessageDeny}
            return func

        return decorator

    def message_allow(self):
        def decorator(func):
            self.events[EventList.MESSAGE_ALLOW] = {"call": func, "data": MessageAllow}
            return func

        return decorator

    def photo_new(self):
        def decorator(func):
            self.events[EventList.PHOTO_NEW] = {"call": func, "data": Photo}
            return func

        return decorator

    def photo_comment_new(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_NEW] = {
                "call": func,
                "data": PhotoComment,
            }
            return func

        return decorator

    def photo_comment_edit(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_EDIT] = {
                "call": func,
                "data": PhotoComment,
            }
            return func

        return decorator

    def photo_comment_restore(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_RESTORE] = {
                "call": func,
                "data": PhotoComment,
            }
            return func

        return decorator

    def photo_comment_delete(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_DELETE] = {
                "call": func,
                "data": PhotoCommentDelete,
            }
            return func

        return decorator

    def audio_new(self):
        def decorator(func):
            self.events[EventList.AUDIO_NEW] = {"call": func, "data": Audio}
            return func

        return decorator

    def video_new(self):
        def decorator(func):
            self.events[EventList.VIDEO_NEW] = {"call": func, "data": Video}
            return func

        return decorator

    def video_comment_new(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_NEW] = {
                "call": func,
                "data": VideoComment,
            }
            return func

        return decorator

    def video_comment_edit(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_EDIT] = {
                "call": func,
                "data": VideoComment,
            }
            return func

        return decorator

    def video_comment_restore(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_RESTORE] = {
                "call": func,
                "data": VideoComment,
            }
            return func

        return decorator

    def video_comment_delete(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_DELETE] = {
                "call": func,
                "data": VideoCommentDelete,
            }
            return func

        return decorator

    def wall_post_new(self):
        def decorator(func):
            self.events[EventList.WALL_POST_NEW] = {"call": func, "data": WallPostNew}
            return func

        return decorator

    def wall_repost(self):
        def decorator(func):
            self.events[EventList.WALL_REPOST] = {"call": func, "data": WallPostNew}
            return func

        return decorator

    def wall_reply_new(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_NEW] = {"call": func, "data": WallReplyNew}
            return func

        return decorator

    def wall_reply_edit(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_EDIT] = {
                "call": func,
                "data": WallReplyNew,
            }
            return func

        return decorator

    def wall_reply_restore(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_RESTORE] = {
                "call": func,
                "data": WallReplyNew,
            }
            return func

        return decorator

    def wall_reply_delete(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_DELETE] = {
                "call": func,
                "data": WallReplyDelete,
            }
            return func

        return decorator

    def board_post_new(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_NEW] = {"call": func, "data": BoardPostNew}
            return func

        return decorator

    def board_post_edit(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_EDIT] = {
                "call": func,
                "data": BoardPostNew,
            }
            return func

        return decorator

    def board_post_restore(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_RESTORE] = {
                "call": func,
                "data": BoardPostNew,
            }
            return func

        return decorator

    def board_post_delete(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_DELETE] = {
                "call": func,
                "data": BoardPostDelete,
            }
            return func

        return decorator

    def market_comment_new(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_NEW] = {
                "call": func,
                "data": MarketCommentNew,
            }
            return func

        return decorator

    def market_comment_edit(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_EDIT] = {
                "call": func,
                "data": MarketCommentNew,
            }
            return func

        return decorator

    def market_comment_restore(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_RESTORE] = {
                "call": func,
                "data": MarketCommentNew,
            }
            return func

        return decorator

    def market_comment_delete(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_DELETE] = {
                "call": func,
                "data": MarketCommentDelete,
            }
            return func

        return decorator

    def group_join(self):
        def decorator(func):
            self.events[EventList.GROUP_JOIN] = {"call": func, "data": GroupJoin}
            return func

        return decorator

    def group_leave(self):
        def decorator(func):
            self.events[EventList.GROUP_JOIN] = {"call": func, "data": GroupLeave}
            return func

        return decorator

    def user_block(self):
        def decorator(func):
            self.events[EventList.USER_BLOCK] = {"call": func, "data": UserBlock}
            return func

        return decorator

    def user_unblock(self):
        def decorator(func):
            self.events[EventList.USER_UNBLOCK] = {"call": func, "data": UserUnblock}
            return func

        return decorator

    def poll_vote_new(self):
        def decorator(func):
            self.events[EventList.POLL_VOTE_NEW] = {"call": func, "data": PollVoteNew}
            return func

        return decorator

    def group_officers_edit(self):
        def decorator(func):
            self.events[EventList.GROUP_OFFICERS_EDIT] = {
                "call": func,
                "data": GroupOfficersEdit,
            }
            return func

        return decorator

    def group_change_settings(self):
        def decorator(func):
            self.events[EventList.GROUP_CHANGE_SETTINGS] = {
                "call": func,
                "data": GroupChangeSettings,
            }
            return func

        return decorator

    def group_change_photo(self):
        def decorator(func):
            self.events[EventList.GROUP_CHANGE_PHOTO] = {
                "call": func,
                "data": GroupLeave,
            }
            return func

        return decorator
