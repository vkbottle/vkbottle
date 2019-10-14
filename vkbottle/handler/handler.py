from typing import Union
from .regex import vbml_parser, re_parser
from .events import Event
from ..utils import dict_of_dicts_merge, Logger


class Handler(object):
    def __init__(self, logger: Logger, group_id: int = 0):
        self.__group_id: int = group_id

        self.message: MessageHandler = MessageHandler()
        self.chat_message: MessageHandler = MessageHandler()
        self.message_both: MessageHandler = MessageHandler()
        self.__undefined_message_func = None

        self.event: Event = Event()
        self.__chat_action_types: dict = dict()

    def dispatch(self):
        self.message.inner = dict_of_dicts_merge(self.message.inner, self.message_both.inner)
        self.chat_message.inner = dict_of_dicts_merge(self.chat_message.inner, self.message_both.inner)

    def chat_action(self, type_: str, rules: dict = None):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """

        def decorator(func):
            self.__chat_action_types[type_] = {'call': func, 'rules': rules or {}}
            return func
        return decorator

    def message_undefined(self):
        """
        If private message is not in message processor this single function will be caused
        """
        def decorator(func):
            self.__undefined_message_func = func
            return func
        return decorator

    def chat_mention(self):
        def decorator(func):
            pattern = re_parser(r'\[(club|public){}\|.*?]'.format(self.__group_id))
            self.chat_message.inner[pattern] = dict(call=func, validators={})
            return func
        return decorator

    def chat_invite(self):
        def decorator(func):
            self.__chat_action_types['chat_invite_user'] = {'call': func, 'rules': {'member_id': -self.__group_id}}
            return func
        return decorator

    @property
    def undefined_func(self):
        return self.__undefined_message_func

    @property
    def chat_action_types(self):
        return self.__chat_action_types


class MessageHandler:
    def __init__(self):
        self.inner = dict()

    def __call__(self, text: str):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        """

        def decorator(func):
            pattern, validators = vbml_parser(text, '{}$')
            self.inner[pattern] = dict(call=func, validators=validators)
            return func

        return decorator

    def startswith(self, text: str):
        """
        Startswith regex message processor

        For example:
        >>> @bot.on.message.startswith(text)

        :param text: text which message should start
        """

        def decorator(func):
            pattern, validators = vbml_parser(text, '{}.*?')
            self.inner[pattern] = dict(call=func, validators=validators)
            return func

        return decorator

    def regex(self, pattern: str):
        """
        Regex message compiler
        :param pattern: Regex string
        """

        def decorator(func):
            self.inner[re_parser(pattern)] = dict(call=func, validators={})
            return func

        return decorator

    def lower(self, text: str):
        """
        Ignore-case message compiler
        :param text:
        :return:
        """
        def decorator(func):
            pattern, validators = vbml_parser(text, '(?i){}$')
            self.inner[pattern] = dict(call=func, validators=validators)
            return func

        return decorator
