from typing import Union
from .regex import vbml_parser, re_parser
from .events import Event
from ..utils import dict_of_dicts_merge, Logger
from inspect import signature


def tupled_dict(tupled: list):
    adict = dict()
    for t in tupled:
        if type(t) is tuple:
            adict[t[0]] = t[1]
        else:
            adict[t] = None

    return adict


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
        self.message.inner = dict_of_dicts_merge(
            self.message.inner, self.message_both.inner
        )
        self.chat_message.inner = dict_of_dicts_merge(
            self.chat_message.inner, self.message_both.inner
        )

    def change_prefix_for_all(self, prefix: list):
        self.message.prefix = prefix
        self.chat_message.prefix = prefix
        self.message_both.prefix = prefix

    def chat_action(self, type_: str, rules: dict = None):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """

        def decorator(func):
            self.__chat_action_types[type_] = {"call": func, "rules": rules or {}}
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
            pattern = re_parser(r"\[(club|public){}\|.*?]".format(self.__group_id))
            ignore_ans = (
                    len(signature(func).parameters) < 1
            )
            self.chat_message.inner[pattern] = dict(call=func, validators={}, ignore_ans=ignore_ans)
            return func

        return decorator

    def chat_invite(self):
        def decorator(func):
            self.__chat_action_types["chat_invite_user"] = {
                "call": func,
                "rules": {"member_id": -self.__group_id},
            }
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
        self.prefix: list = ["/", "!"]

    def __call__(self, text: str, command: bool = False, lower: bool = False):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            pattern, validators, arguments = vbml_parser(
                text,
                ("(?i)" if lower else "") + "{}$",
                prefix=self.prefix if command else None,
            )
            ignore_ans = (
                len([a for a in signature(func).parameters if a not in arguments]) < 1
            )
            self.inner[pattern] = dict(
                call=func, validators=validators, ignore_ans=ignore_ans
            )
            return func

        return decorator

    def startswith(self, text: str, command=False, lower: bool = False):
        """
        Startswith regex message processor

        For example:
        >>> @bot.on.message.startswith(text)

        :param text: text which message should start
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            pattern, validators, arguments = vbml_parser(
                text,
                ("(?i)" if lower else "") + "{}.*?",
                prefix=self.prefix if command else None,
            )
            ignore_ans = (
                len([a for a in signature(func).parameters if a not in arguments]) < 1
            )
            self.inner[pattern] = dict(
                call=func, validators=validators, ignore_ans=ignore_ans
            )
            return func

        return decorator

    def regex(self, pattern: str):
        """
        Regex message compiler
        :param pattern: Regex string
        """

        def decorator(func):
            ignore_ans = len(signature(func).parameters) < 1
            self.inner[re_parser(pattern)] = dict(
                call=func, validators={}, ignore_ans=ignore_ans
            )
            return func

        return decorator
