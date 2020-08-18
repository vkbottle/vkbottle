import typing
import inspect
import re

from copy import copy
from vbml import Pattern, Patcher
from html import unescape

from vkbottle.types.message import Message as BotMessage
from vkbottle.types.user_longpoll import Message as UserMessage
from vkbottle.types import user_longpoll
from vkbottle.utils import flatten, json

Message = typing.Union[BotMessage, UserMessage]


class Copy:
    def copy(self):
        return copy(self)


class RuleExecute:
    def __init__(self):
        self.args = []
        self.kwargs = {}

    def update(self, args: list, kwargs: dict):
        self.args.extend(args)
        self.kwargs.update(kwargs)

    def __call__(self):
        return self.args, self.kwargs

    def __repr__(self):
        return f"<{self.args}{self.kwargs}>"


class AbstractRule(Copy):
    call: typing.Callable
    getfullargspec: inspect.FullArgSpec

    def __init_subclass__(cls, **kwargs):
        cls.context: RuleExecute = RuleExecute()
        cls.watch_context = None

    def create(self, func: typing.Callable, data: dict = None):
        self.call: typing.Callable = func
        if data is not None:
            setattr(self, "data", {**getattr(self, "data", {}), **data})
        self.getfullargspec = inspect.getfullargspec(self.call)

    def resolve(self, value):
        if self.watch_context:
            context = self.watch_context.get(value)

            if isinstance(context, (list, tuple)):
                self.context.args.extend(context)
            elif isinstance(context, dict):
                self.context.kwargs.update(context)
            else:
                self.context.args.append(context)

    async def __call__(self, event):
        self.__init_subclass__()
        return await self.check(event)

    async def check(self, event) -> bool:
        ...

    def __repr__(self):
        return f"<Rule {self.__class__.__qualname__} context={self.context}>"


class Any(AbstractRule):
    async def check(self, event) -> bool:
        return True


class AbstractMessageRule(AbstractRule):
    async def check(self, message: Message) -> bool:
        ...


class UnionMixin(AbstractMessageRule):
    def __init__(self, mixin=None):
        mixin = mixin if mixin is not None else []
        if not isinstance(mixin, list):
            mixin = [mixin]
        self.data = {"mixin": mixin}


class StickerRule(UnionMixin):
    async def check(self, message: Message) -> bool:
        if message.attachments and message.attachments[0].sticker:
            if not self.data["mixin"]:
                return True
            if message.attachments[0].sticker.sticker_id in self.data["mixin"]:
                return True


class FromMe(AbstractMessageRule):
    def __init__(self, from_me: bool = True):
        self.from_me = from_me

    async def check(self, message: Message) -> bool:
        if (message.from_id == await message.api.user_id) is self.from_me:
            return True


class MessageRule(AbstractMessageRule):
    def __init__(self, message: typing.Union[str, typing.List[str]]):
        if isinstance(message, str):
            message = [message]
        self.data = {"message": message}

    async def check(self, message: Message) -> bool:
        if message.text in self.data["message"]:
            return True


class LevenshteinDisRule(AbstractMessageRule):
    def __init__(self, mixin: typing.Union[str, typing.List[str]], lev_d: float = 1):
        if isinstance(mixin, dict):
            self.watch_context = mixin
            mixin = list(mixin.keys())
        elif not isinstance(mixin, list):
            mixin = [mixin]
        self.data = {"samples": mixin}
        self.lev = lev_d

    @staticmethod
    def distance(a, b):
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = (
                    previous_row[j] + 1,
                    current_row[j - 1] + 1,
                    previous_row[j - 1],
                )
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    async def check(self, message: Message) -> bool:
        for sample in self.data["samples"]:
            if self.distance(message.text, sample) <= self.lev:
                self.resolve(sample)
                return True


class CommandRule(AbstractMessageRule):
    def __init__(
        self,
        message: typing.Union[str, typing.List[str]],
        prefixes: typing.Tuple[str, ...] = ("/", "!"),
    ):
        if isinstance(message, dict):
            self.watch_context = message
            message = list(message.keys())
        elif not isinstance(message, list):
            message = [message]
        self.data = {"message": message, "prefixes": prefixes}

    async def check(self, message: Message) -> bool:
        if not message.text or len(message.text) < 2:
            return
        prefix, text = message.text[0], message.text[1:]
        return prefix in self.data["prefixes"] and text in self.data["message"]


class EventRule(AbstractRule):
    def __init__(self, event: typing.Union[str, typing.List[str]]):
        if isinstance(event, str):
            event = [event]
        self.data = {"event": event}

    async def check(self, event) -> bool:
        if "data" not in self.data:
            self.data["data"] = self.getfullargspec.annotations.get(
                self.getfullargspec.args[0], dict
            )
        for e in self.data["event"]:
            if e == event:
                return True


class UserLongPollEventRule(AbstractRule):
    def __init__(self, event: typing.Union[int, typing.List[int]], *rules):
        if isinstance(event, int):
            event = [event]
        self.data = {"event": event, "rules": rules}

    async def check(self, update):
        for e in self.data["event"]:
            if e == update[0]:
                if not self.data["rules"]:
                    return True
                return tuple(self.data["rules"])


class UserMessageRule(UnionMixin):
    async def check(self, message: user_longpoll.Message):
        if message.text in self.data["mixin"]:
            return True


class ChatMessage(AbstractMessageRule):
    async def check(self, message: Message) -> bool:
        if message.peer_id > 2e9:
            return True


class PrivateMessage(AbstractMessageRule):
    async def check(self, message: Message) -> bool:
        if message.peer_id < 2e9:
            return True


class VBML(AbstractMessageRule):
    def __init__(
        self,
        pattern: typing.Union[
            str,
            Pattern,
            typing.List[typing.Union[str, Pattern]],
            typing.Dict[typing.Union[str, Pattern], typing.Union[list, dict]],
        ],
        lower: bool = None,
    ):
        if isinstance(pattern, dict):
            self.watch_context = pattern
            pattern = list(pattern)
        self._patcher = Patcher.get_current()
        patterns: typing.List[Pattern] = []
        if isinstance(pattern, Pattern):
            patterns = [pattern]
        elif isinstance(pattern, list):
            for p in pattern:
                if isinstance(p, str):
                    patterns.append(
                        self._patcher.pattern(p, flags=re.IGNORECASE if lower else None)
                    )
                else:
                    patterns.append(p)
        elif isinstance(pattern, str):
            patterns = [
                self._patcher.pattern(pattern, flags=re.IGNORECASE if lower else None)
            ]

        self.data = {"pattern": patterns}


class VBMLRule(VBML):
    async def check(self, message: Message) -> bool:
        patterns: typing.List[Pattern] = self.data["pattern"]
        message = message.text.replace("<br>", "\n")
        message = unescape(message)

        for pattern in patterns:
            if self._patcher.check(message, pattern) is not None:
                self.context.kwargs = pattern.dict()
                self.resolve(pattern)
                return True


class AttachmentRule(UnionMixin):
    async def check(self, message: Message) -> bool:
        attachments = flatten(
            [
                list(attachment.dict(skip_defaults=True).keys())
                for attachment in message.attachments
            ]
        )
        if attachments and not self.data["mixin"]:
            # ANY ATTACHMENTS
            return True
        for attachment_type in self.data.get("mixin", []):
            if attachment_type in attachments:
                return True


class ChatActionRule(AbstractMessageRule):
    def __init__(
        self, chat_action: typing.Union[str, typing.List[str]], rules: dict = None
    ):
        if isinstance(chat_action, str):
            chat_action = [chat_action]
        self.data = dict()
        self.data["chat_action"] = chat_action
        self.data["rules"] = rules or {}

    async def check(self, message: Message) -> bool:
        if message.action:
            if message.action.type in self.data["chat_action"]:
                if {
                    **message.action.dict(skip_defaults=True),
                    **self.data["rules"],
                } == message.action.dict(skip_defaults=True):
                    return True


class PayloadRule(AbstractMessageRule):
    def __init__(self, payload: dict, mode=1):
        self.data = dict()
        self.data["payload"] = payload
        self.data["mode"] = mode

    @staticmethod
    def dispatch(payload: str) -> dict:
        try:
            return json.loads(payload)
        except json.decoder.JSONDecodeError:
            return dict()

    async def check(self, message: Message) -> bool:
        if message.payload is not None:
            payload = self.dispatch(message.payload)
            if self.data["mode"] == 1:
                # EQUALITY
                if payload == self.data["payload"]:
                    return True
            elif self.data["mode"] == 2:
                # CONTAIN
                if {**payload, **self.data["payload"]} == payload:
                    return True
