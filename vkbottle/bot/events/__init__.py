"""Read LICENSE.txt"""

"""
VKBOTTLE EVENTS TYPES
"""

from ...utils import Logger, make_priority_path, dict_of_dicts_merge

from ...notifications import add_undefined

from .events import OnMessage, OnMessageChat, OnMessageBoth, Event

import re


class Events:
    def __init__(self, group_id: int, logger: Logger = Logger(True), use_regex: bool = True):
        """
        Make decorator processors (dictionaries with functions)
        :param logger: Logging object
        :param use_regex: More comfortable with regex, but if speed is main priority...
        fixme RU - не доделал это..
        """
        # Collections
        self.use_regex = use_regex

        self.group_id = group_id

        # Processors
        self.processor_message_regex = {}

        self.processor_message_chat_regex = {}

        self.undefined_message_func = (lambda *args: logger.warn(add_undefined))

        self.events = {}

        self.chat_action_types = {}

        # Decorators
        self.message = OnMessage(self)

        self.message_chat = OnMessageChat(self)

        self.message_both = OnMessageBoth(self)

        self.event = Event(self)

    def merge_processors(self):
        """
        Merge message decorators with message-both decorators. Using deepcopy and MutableMapping to merge dictionaries
        own priorities
        todo RU - исправить эту неприятную жижу
        """
        self.processor_message_regex = dict_of_dicts_merge(self.message.processor, self.message_both.processor_message)
        self.processor_message_chat_regex = dict_of_dicts_merge(self.message_chat.processor, self.message_both.processor_chat)
        self.events = self.event.events

    def chat_action(self, type_: str, rules: dict = None):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """
        rules = {} if not rules else rules

        def decorator(func):
            self.chat_action_types[type_] = {'call': func, 'rules': rules}
            return func
        return decorator

    def message_undefined(self):
        """
        If private message is not in message processor this single function will be caused
        """
        def decorator(func):
            self.undefined_message_func = func
            return func
        return decorator

    def chat_mention(self):
        def decorator(func):
            pattern = re.compile(r'\[(club|public)' + str(self.group_id) + r'\|.*?]')
            self.processor_message_chat_regex = make_priority_path(self.processor_message_chat_regex, 0, pattern, func)
            return func
        return decorator

    def chat_invite(self):
        def decorator(func):
            self.chat_action_types['chat_invite_user'] = {'call': func, 'rules': {'member_id': self.group_id * -1}}
            return func
        return decorator
