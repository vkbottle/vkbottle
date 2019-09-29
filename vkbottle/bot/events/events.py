"""Read LICENSE.txt"""


from ...utils import make_priority_path

from ...vktypes.types.events.community.events_objects import *
from ...vktypes.types.events.community.events_list import EventList
from ...vktypes.types.message import Message
from ...vktypes.types.attachments.photo import Photo
from ...vktypes.types.attachments.audio import Audio
from ...vktypes.types.attachments.video import Video

import re


def regex_message(text, formatted_pattern='{}'):
    """Allow to generate REGEX patterns for message matching"""

    escape = {ord(x): '\\' + x for x in r'\.*+?()[]|^$'}
    typed_patterns = re.findall(r'(<([a-zA-Z0-9_]+)+:.*?>)', text.translate(escape))
    validators: dict = {}

    for p in typed_patterns:
        validators_of_pattern = re.findall(r':([a-zA-Z0-9_]+)+', p[0])
        validators[p[1]] = validators_of_pattern
        text = re.sub(':.*?>', '>', text.translate(escape))

    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text.translate(escape))
    return re.compile(formatted_pattern.format(pattern)), validators


class OnMessage(object):
    """
    OnMessage decorator wrapper. Needed for regex processing and advanced features support
    todo RU - покрасить забор
    """
    def __init__(self, events):
        self.processor = events.processor_message_regex

    def __call__(self, text: str, priority: int = 0):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern, validators = regex_message(text)
            self.processor = make_priority_path(self.processor,
                                                priority, pattern, dict(call=func, validators=validators))
            return func
        return decorator

    def startswith(self, text: str, priority: int = 0):
        """
        Startswith regex message processor

        For example:
        @bot.on.message.startswith(text)

        :param text: text which message should start
        :param priority: priority of checkup processor
        """
        def decorator(func):

            pattern, validators = regex_message(text, formatted_pattern='{}.*?')

            self.processor = make_priority_path(
                  self.processor,
                  priority, pattern,
                  dict(call=func, validators=validators)
            )

            return func

        return decorator

    def regex(self, pattern: str, priority: int = 0):
        """
        Regex message compiler
        :param pattern: Regex string
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator

    def lower(self, text: str, priority: int = 0):
        def decorator(func):
            pattern, validators = regex_message(text, formatted_pattern='(?i){}')
            self.processor = make_priority_path(self.processor,
                                                priority, pattern,
                                                dict(call=func, validators=validators))
            return func
        return decorator


class OnMessageChat(object):
    """
    OnMessage in chat decorator wrapper. Needed for regex processing and advanced features support
    """
    def __init__(self, events):
        self.processor = events.processor_message_chat_regex

    def __call__(self, text: str, priority: int = 0):
        """
        Simple on.message_chat(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern, validators = regex_message(text)
            self.processor = make_priority_path(self.processor,
                                                priority, pattern, dict(call=func, validators=validators))
            return func
        return decorator

    def startswith(self, text: str, priority: int = 0):
        """
        Startswith regex message processor

        For example:
        @bot.on.message_chat.startswith(text)

        :param text: text which message should start
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern, validators = regex_message(text, formatted_pattern='{}.*?')

            self.processor = make_priority_path(
                self.processor,
                priority, pattern,
                dict(call=func, validators=validators)
            )
            return func
        return decorator

    def regex(self, pattern: str, priority: int = 0):
        """
        Regex message compiler
        :param pattern: Regex string
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator

    def lower(self, text: str, priority: int = 0):
        def decorator(func):
            pattern, validators = regex_message(text, formatted_pattern='(?i){}')
            self.processor = make_priority_path(self.processor,
                                                priority, pattern,
                                                dict(call=func, validators=validators))
            return func
        return decorator


class OnMessageBoth(object):
    """
    On private and in chat message decorator wrapper. Needed for regex processing and advanced features support
    """
    def __init__(self, events):
        self.processor_message = events.processor_message_regex
        self.processor_chat = events.processor_message_regex

    def __call__(self, text, priority: int = 0):
        """
        Simple on.message_both(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern, validators = regex_message(text)
            self.processor_message = make_priority_path(self.processor_message,
                                                priority, pattern, dict(call=func, validators=validators))
            self.processor_chat = make_priority_path(self.processor_chat,
                                                        priority, pattern, dict(call=func, validators=validators))
            return func
        return decorator

    def startswith(self, text, priority: int = 0):
        """
        Startswith regex message processor

        For example:
        @bot.on.message_both.startswith(text)

        :param text: text which message should start
        :param priority: priority of checkup processor
        """
        def decorator(func):
            pattern, validators = regex_message(text, formatted_pattern='{}.*?')

            self.processor_message = make_priority_path(self.processor_message,
                                                        priority, pattern, dict(call=func, validators=validators))
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     priority, pattern, dict(call=func, validators=validators))
            return func
        return decorator

    def regex(self, pattern, priority: int = 0):
        """
        Regex message compiler
        :param pattern: Regex string
        :param priority: priority of checkup processor
        """
        def decorator(func):
            self.processor_message = make_priority_path(self.processor_message,
                                                        priority, re.compile(pattern),
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     priority, re.compile(pattern),
                                                     func)
            return func
        return decorator

    def lower(self, text: str, priority: int = 0):
        def decorator(func):
            pattern, validators = regex_message(text, formatted_pattern='(?i){}')
            self.processor_message = make_priority_path(self.processor_message,
                                                        priority, pattern, dict(call=func, validators=validators))
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     priority, pattern, dict(call=func, validators=validators))
            return func
        return decorator


class Event(object):
    def __init__(self, events):
        self.events = events.events

    def message_reply(self):
        def decorator(func):
            self.events[EventList.MESSAGE_REPLY] = {'call': func, 'data': Message}
            return func
        return decorator

    def message_deny(self):
        def decorator(func):
            self.events[EventList.MESSAGE_DENY] = {'call': func, 'data': MessageDeny}
            return func
        return decorator

    def message_allow(self):
        def decorator(func):
            self.events[EventList.MESSAGE_ALLOW] = {'call': func, 'data': MessageAllow}
            return func
        return decorator

    def photo_new(self):
        def decorator(func):
            self.events[EventList.PHOTO_NEW] = {'call': func, 'data': Photo}
            return func
        return decorator

    def photo_comment_new(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_NEW] = {'call': func, 'data': PhotoComment}
            return func
        return decorator

    def photo_comment_edit(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_EDIT] = {'call': func, 'data': PhotoComment}
            return func
        return decorator

    def photo_comment_restore(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_RESTORE] = {'call': func, 'data': PhotoComment}
            return func
        return decorator

    def photo_comment_delete(self):
        def decorator(func):
            self.events[EventList.PHOTO_COMMENT_DELETE] = {'call': func, 'data': PhotoCommentDelete}
            return func
        return decorator

    def audio_new(self):
        def decorator(func):
            self.events[EventList.AUDIO_NEW] = {'call': func, 'data': Audio}
            return func
        return decorator

    def video_new(self):
        def decorator(func):
            self.events[EventList.VIDEO_NEW] = {'call': func, 'data': Video}
            return func
        return decorator

    def video_comment_new(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_NEW] = {'call': func, 'data': VideoComment}
            return func
        return decorator

    def video_comment_edit(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_EDIT] = {'call': func, 'data': VideoComment}
            return func
        return decorator

    def video_comment_restore(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_RESTORE] = {'call': func, 'data': VideoComment}
            return func
        return decorator

    def video_comment_delete(self):
        def decorator(func):
            self.events[EventList.VIDEO_COMMENT_DELETE] = {'call': func, 'data': VideoCommentDelete}
            return func
        return decorator

    def wall_post_new(self):
        def decorator(func):
            self.events[EventList.WALL_POST_NEW] = {'call': func, 'data': WallPostNew}
            return func
        return decorator

    def wall_repost(self):
        def decorator(func):
            self.events[EventList.WALL_REPOST] = {'call': func, 'data': WallPostNew}
            return func
        return decorator

    def wall_reply_new(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_NEW] = {'call': func, 'data': WallReplyNew}
            return func
        return decorator

    def wall_reply_edit(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_EDIT] = {'call': func, 'data': WallReplyNew}
            return func
        return decorator

    def wall_reply_restore(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_RESTORE] = {'call': func, 'data': WallReplyNew}
            return func
        return decorator

    def wall_reply_delete(self):
        def decorator(func):
            self.events[EventList.WALL_REPLY_DELETE] = {'call': func, 'data': WallReplyDelete}
            return func
        return decorator

    def board_post_new(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_NEW] = {'call': func, 'data': BoardPostNew}
            return func
        return decorator

    def board_post_edit(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_EDIT] = {'call': func, 'data': BoardPostNew}
            return func
        return decorator

    def board_post_restore(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_RESTORE] = {'call': func, 'data': BoardPostNew}
            return func
        return decorator

    def board_post_delete(self):
        def decorator(func):
            self.events[EventList.BOARD_POST_DELETE] = {'call': func, 'data': BoardPostDelete}
            return func
        return decorator

    def market_comment_new(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_NEW] = {'call': func, 'data': MarketCommentNew}
            return func
        return decorator

    def market_comment_edit(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_EDIT] = {'call': func, 'data': MarketCommentNew}
            return func
        return decorator

    def market_comment_restore(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_RESTORE] = {'call': func, 'data': MarketCommentNew}
            return func
        return decorator

    def market_comment_delete(self):
        def decorator(func):
            self.events[EventList.MARKET_COMMENT_DELETE] = {'call': func, 'data': MarketCommentDelete}
            return func
        return decorator

    def group_join(self):
        def decorator(func):
            self.events[EventList.GROUP_JOIN] = {'call': func, 'data': GroupJoin}
            return func
        return decorator

    def group_leave(self):
        def decorator(func):
            self.events[EventList.GROUP_JOIN] = {'call': func, 'data': GroupLeave}
            return func
        return decorator

    def user_block(self):
        def decorator(func):
            self.events[EventList.USER_BLOCK] = {'call': func, 'data': UserBlock}
            return func
        return decorator

    def user_unblock(self):
        def decorator(func):
            self.events[EventList.USER_UNBLOCK] = {'call': func, 'data': UserUnblock}
            return func
        return decorator

    def poll_vote_new(self):
        def decorator(func):
            self.events[EventList.POLL_VOTE_NEW] = {'call': func, 'data': PollVoteNew}
            return func
        return decorator

    def group_officers_edit(self):
        def decorator(func):
            self.events[EventList.GROUP_OFFICERS_EDIT] = {'call': func, 'data': GroupOfficersEdit}
            return func
        return decorator

    def group_change_settings(self):
        def decorator(func):
            self.events[EventList.GROUP_CHANGE_SETTINGS] = {'call': func, 'data': GroupChangeSettings}
            return func
        return decorator

    def group_change_photo(self):
        def decorator(func):
            self.events[EventList.GROUP_CHANGE_PHOTO] = {'call': func, 'data': GroupLeave}
            return func
        return decorator
