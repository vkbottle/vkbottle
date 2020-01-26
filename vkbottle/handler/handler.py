from .events import Event
from ..utils import Logger
from inspect import signature
import typing
from ..const import __version__
from inspect import iscoroutinefunction
from ..api import HandlerError
import re
from ..framework.rule import AbstractRule, VBMLRule, ChatActionRule, PayloadRule
from vbml import Patcher, Pattern


def should_ignore_ans(func: typing.Callable, arguments: list) -> bool:
    if not iscoroutinefunction(func):
        raise HandlerError("Handling functions must be async")
    return len([a for a in signature(func).parameters if a not in arguments]) < 1


class Handler(object):
    def __init__(self, logger: Logger, group_id: int = 0):
        self.__group_id: int = group_id
        self.__logger = logger

        self.message: MessageHandler = MessageHandler()
        self.chat_message: MessageHandler = MessageHandler()
        self.message_both: MessageHandler = MessageHandler()
        self.event: Event = Event()

        self._pre_p: typing.Optional[typing.Callable] = None
        self.__undefined_message_func = None
        self._patcher = Patcher.get_current()

        if not hasattr(Pattern, "context_copy"):
            raise RuntimeError(
                "\n\n\tNow! Update vbml with command:\n"
                "\tpip install https://github.com/timoniq/vbml/archive/master.zip --upgrade\n"
                "\ttnx <3"
            )

    def concatenate(self, handler: "Handler"):
        """
        Concatenate handlers from current handler and another handler
        :param handler: another handler
        :return:
        """
        self.message.concatenate(handler.message)
        self.chat_message.concatenate(handler.chat_message)
        self.message_both.concatenate(handler.message_both)
        self.event.rules += handler.event.rules

        if self.pre is None:
            self._pre_p = handler.pre

    async def dispatch(self, get_current_rest: typing.Callable = None) -> None:
        """
        Dispatch handlers from only-handlers and both-handlers
        :param get_current_rest: REST from vkbottle-rest
        :return:
        """

        self.message.rules += self.message_both.rules
        self.chat_message.rules += self.message_both.rules

        self.message.payload.rules += self.message_both.payload.rules
        self.chat_message.payload.rules += self.message_both.payload.rules

        if get_current_rest:

            # Check updates from timoniq/vkbottle-rest
            current_rest = await get_current_rest()
            if current_rest["version"] != __version__:
                self.__logger.mark(
                    "You are using old version of VKBottle. Update is found: {}".format(
                        current_rest["version"]
                    ),
                    current_rest["description"],
                )

    def change_prefix_for_all(self, prefix: list) -> None:
        self.message.prefix = prefix
        self.chat_message.prefix = prefix
        self.message_both.prefix = prefix

    def chat_action(
        self, type_: typing.Union[str, typing.List[str]], rules: dict = None
    ):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """

        def decorator(func):
            rule = ChatActionRule(type_, rules=rules)
            rule.create(func)
            self.chat_message.rules.append([rule])
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
            pattern = self._patcher.pattern(
                pattern="", _pattern=r"\[(club|public){}\|.*?]".format(self.__group_id)
            )
            ignore_ans = len(signature(func).parameters) < 1

            rule = VBMLRule(pattern)
            rule.create(func, {"ignore_ans": ignore_ans})
            self.chat_message.rules.append([rule])
            return func

        return decorator

    def chat_invite(self):
        def decorator(func):
            rule = ChatActionRule("chat_invite_user", {"member_id": -self.__group_id})
            rule.create(func)
            self.chat_message.rules.append([rule])
            return func

        return decorator

    @property
    def undefined_func(self):
        return self.__undefined_message_func

    @property
    def pre(self):
        return self._pre_p

    def pre_process(self):
        def decorator(func):
            self._pre_p = func
            return func

        return decorator


class MessageHandler:
    def __init__(self):
        self.payload: PayloadHandler = PayloadHandler()
        self.rules: typing.List[typing.List[AbstractRule]] = list()
        self.prefix: list = ["/", "!"]
        self._patcher = Patcher.get_current()

    def concatenate(self, message_handler: "MessageHandler"):
        self.rules += message_handler.rules
        self.prefix += [p for p in message_handler.prefix if p not in self.prefix]
        self.payload.rules += message_handler.payload.rules

    def add_handler(
        self,
        func: typing.Callable,
        *rules,
        text: typing.Union[str, Pattern] = None,
        lower: bool = False,
        command: bool = False,
        pattern: str = None,
    ):
        """
        Add handler to disself._patcher without decorators
        :param text: text (match case)
        :param func: function responsible for event
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        :param pattern: any regex pattern pattern. {} means text which will be formatted
        :return: True
        """
        current: typing.List[AbstractRule] = list()

        if text:
            if not isinstance(text, Pattern):
                prefix = ("[" + "|".join(self.prefix) + "]") if command else ""
                pattern = self._patcher.pattern(
                    text,
                    pattern=(prefix + "{}$") if prefix else pattern,
                    flags=re.IGNORECASE if lower else None,
                )
                rule = VBMLRule(pattern)
                rule.create(func)
                rule.data["ignore_ans"] = should_ignore_ans(func, pattern.arguments)
                current.append(rule)
            else:
                rule = VBMLRule(self._patcher.pattern(text))
                rule.create(func)
                rule.data["ignore_ans"] = should_ignore_ans(func, text.arguments)
                current.append(rule)

        for rule in rules:
            rule.create(func)
            current.append(rule)

        self.rules.append(current)

    def rule(self, *rules):
        def decorator(func):
            self.rules.append([rule.create(func) for rule in rules])
            return func

        return decorator

    def __call__(
        self,
        *rules,
        text: typing.Union[str, Pattern] = None,
        command: bool = False,
        lower: bool = False,
    ):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            current: typing.List[AbstractRule] = list()

            if text:
                if not isinstance(text, Pattern):
                    prefix = ("[" + "|".join(self.prefix) + "]") if command else ""
                    pattern = self._patcher.pattern(
                        text,
                        pattern=(prefix + "{}$") if prefix else "{}$",
                        flags=re.IGNORECASE if lower else None,
                    )
                    rule = VBMLRule(pattern)
                    rule.create(func)
                    rule.data["ignore_ans"] = should_ignore_ans(func, pattern.arguments)
                    current.append(rule)
                else:
                    rule = VBMLRule(self._patcher.pattern(text))
                    rule.create(func)
                    rule.data["ignore_ans"] = should_ignore_ans(func, text.arguments)
                    current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)
            return func

        return decorator

    def startswith(
        self,
        text: typing.Union[str, Pattern],
        *rules,
        command: bool = False,
        lower: bool = False,
    ):
        """
        Startswith regex message processor

        For example:
        >>> # @bot.on.message.startswith(text)

        :param text: text which message should start
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            current: typing.List[AbstractRule] = list()

            if text:
                if not isinstance(text, Pattern):
                    prefix = ("[" + "|".join(
                        self.prefix) + "]") if command else ""
                    pattern = self._patcher.pattern(
                        text,
                        pattern=(prefix + "{}") if prefix else "{}",
                        flags=re.IGNORECASE if lower else None,
                    )
                    rule = VBMLRule(pattern)
                    rule.create(func)
                    rule.data["ignore_ans"] = should_ignore_ans(func, pattern.arguments)
                    current.append(rule)
                else:
                    rule = VBMLRule(self._patcher.pattern(text))
                    rule.create(func)
                    rule.data["ignore_ans"] = should_ignore_ans(func, text.arguments)
                    current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)
            return func

        return decorator

    def regex(self, pattern: str, *rules):
        """
        Regex message compiler
        :param pattern: Regex string
        """

        def decorator(func):
            current = list()

            rule = VBMLRule(self._patcher.pattern("", pattern=pattern))
            rule.create(func)
            rule.data["ignore_ans"] = False
            current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)
            return func

        return decorator


class PayloadHandler:
    def __init__(self):
        self.rules: typing.List[typing.List[AbstractRule]] = list()

    def __call__(self, payload: dict, *rules):
        def decorator(func):
            current = list()

            rule = PayloadRule(payload, mode=1)
            rule.create(func)
            rule.data["ignore_ans"] = False
            current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)

            return func

        return decorator

    def contains(self, payload: dict, *rules):
        def decorator(func):
            current = list()

            rule = PayloadRule(payload, mode=2)
            rule.create(func)
            rule.data["ignore_ans"] = False
            current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)

            return func

        return decorator
