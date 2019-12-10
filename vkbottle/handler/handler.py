from .events import Event
from ..utils import dict_of_dicts_merge, Logger
from inspect import signature
from typing import Callable, Optional, Dict, Union
from ..const import __version__
from inspect import iscoroutinefunction
from ..api import HandlerError
import json
from vbml import Patcher


def should_ignore_ans(func: Callable, arguments: list) -> bool:
    if not iscoroutinefunction(func):
        raise HandlerError("Handling function must be async")
    return len([a for a in signature(func).parameters if a not in arguments]) < 1


class Handler(object):
    def __init__(self, logger: Logger, group_id: int = 0):
        self.__group_id: int = group_id
        self.__logger = logger

        self.message: MessageHandler = MessageHandler()
        self.chat_message: MessageHandler = MessageHandler()
        self.message_both: MessageHandler = MessageHandler()
        self.event: Event = Event()
        self._pre_p: Optional[Callable] = None

        self.__undefined_message_func = None
        self.__chat_action_types: list = list()

        self._patcher = Patcher.get_current()

    async def dispatch(self, get_current_rest: Callable = None) -> None:

        self.message.inner = dict_of_dicts_merge(
            self.message.inner, self.message_both.inner
        )
        self.chat_message.inner = dict_of_dicts_merge(
            self.chat_message.inner, self.message_both.inner
        )

        self.message.payload.inner = dict_of_dicts_merge(
            self.message.payload.inner, self.message_both.payload.inner
        )
        self.chat_message.payload.inner = dict_of_dicts_merge(
            self.chat_message.payload.inner, self.message_both.payload.inner
        )

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

    def chat_action(self, type_: str, rules: dict = None):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """

        def decorator(func):
            self.__chat_action_types.append(
                {"name": type_, "call": func, "rules": rules or {}}
            )
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
                text="", pattern=r"\[(club|public){}\|.*?]".format(self.__group_id)
            )
            ignore_ans = len(signature(func).parameters) < 1
            self.chat_message.inner[pattern] = dict(
                call=func, validators={}, ignore_ans=ignore_ans
            )
            return func

        return decorator

    def chat_invite(self):
        def decorator(func):
            self.__chat_action_types.append(
                {
                    "name": "chat_invite_user",
                    "call": func,
                    "rules": {"member_id": -self.__group_id},
                }
            )
            return func

        return decorator

    @property
    def undefined_func(self):
        return self.__undefined_message_func

    @property
    def chat_action_types(self):
        return self.__chat_action_types

    @property
    def pre(self):
        return self._pre_p

    def any_pre_process(self):
        def decorator(func):
            self._pre_p = func
            return func

        return decorator


class MessageHandler:
    def __init__(self):
        self.inner = dict()
        self.payload = PayloadHandler()
        self.prefix: list = ["/", "!"]
        self._patcher = Patcher.get_current()

    def add_handler(
        self,
        text: str,
        func: Callable,
        command: bool = False,
        lower: bool = False,
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
        prefix = ("[" + "|".join(self.prefix) + "]") if command else ""
        pattern = self._patcher.pattern(
            text, pattern=pattern or ("(?i)" if lower else "") + prefix + "{}$",
        )
        self.inner[pattern] = dict(
            call=func, ignore_ans=should_ignore_ans(func, pattern.arguments)
        )

    def __call__(self, text: str, command: bool = False, lower: bool = False):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            prefix = ("[" + "|".join(self.prefix) + "]") if command else ""
            pattern = self._patcher.pattern(text, pattern=("(?i)" if lower else "") + prefix + "{}$",)
            self.inner[pattern] = dict(
                call=func, ignore_ans=should_ignore_ans(func, pattern.arguments)
            )
            return func

        return decorator

    def startswith(self, text: str, command: bool = False, lower: bool = False):
        """
        Startswith regex message processor

        For example:
        >>> @bot.on.message.startswith(text)

        :param text: text which message should start
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            prefix = ("[" + "|".join(self.prefix) + "]") if command else ""
            pattern = self._patcher.pattern(
                text, pattern=("(?i)" if lower else "") + prefix + "{}.*?",
            )
            self.inner[pattern] = dict(
                call=func, ignore_ans=should_ignore_ans(func, pattern.arguments)
            )
            return func

        return decorator

    def regex(self, pattern: str):
        """
        Regex message compiler
        :param pattern: Regex string
        """

        def decorator(func):
            self.inner[self._patcher.pattern(text="", pattern=pattern)] = dict(
                call=func, ignore_ans=should_ignore_ans(func, [])
            )
            return func

        return decorator


class Payload:
    def __init__(self, payload: dict, mode=1):
        self.payload = payload
        self.mode = mode

    def __call__(self, check: dict):
        if self.mode == 1:
            # EQUAL
            if check == self.payload:
                return True
        elif self.mode == 2:
            # CONTAINS
            if {**check, **self.payload} == check:
                return True


class PayloadHandler:
    def __init__(self):
        self.inner: Dict[Payload] = dict()

    def __call__(self, payload: dict):
        def decorator(func):

            self.inner[Payload(payload)] = dict(
                call=func, ignore_ans=should_ignore_ans(func, [])
            )

            return func
        return decorator

    def contains(self, payload: dict):
        def decorator(func):

            self.inner[Payload(payload, 2)] = dict(
                call=func, ignore_ans=should_ignore_ans(func, [])
            )

            return func

        return decorator


class DescribedHandler:
    described_handlers_by_func: Dict[Callable, Dict] = {}
    described_handlers_by_name: Dict[Callable, Dict] = {}

    def __init__(self):
        pass

    def __call__(self, name: str = None, description: str = None):
        def decorator(func):

            self.described_handlers_by_func[func] = dict(
                name=name or "", description=description or ""
            )
            if name:
                self.described_handlers_by_name[name] = dict(
                    name=name or "", description=description or ""
                )
            return func

        return decorator

    def get(self, name: Union[Callable, str], default=None):
        if isinstance(name, Callable):
            return self.described_handlers_by_func.get(name, default)
        return self.described_handlers_by_name.get(name, default)
