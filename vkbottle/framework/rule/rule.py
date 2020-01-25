from ...types import Message
from vbml import Pattern, Patcher
import typing
import json


class RuleExecute:
    def __init__(self):
        self.args = []
        self.kwargs = {}


class AbstractRule:
    def __init_subclass__(cls, **kwargs):
        cls.call: typing.Optional[typing.Callable] = None
        cls.context: RuleExecute = RuleExecute()

    def create(self, func: typing.Callable, data: dict = None):
        self.call: typing.Callable = func
        self.context = RuleExecute()
        if data is not None:
            setattr(self, "data", {**getattr(self, "data", {}), **data})
        ...

    def check(self, event):
        ...


class AbstractMessageRule(AbstractRule):
    def check(self, message: Message):
        ...


class UnionMixin(AbstractMessageRule):
    def __init__(self, mixin=None):
        mixin = mixin if mixin is not None else []
        if not isinstance(mixin, list):
            mixin = [mixin]
        self.data = {"mixin": mixin}


class StickerRule(UnionMixin):
    def check(self, message: Message):
        if len(message.attachments) and message.attachments[0].sticker:
            if not len(self.data["mixin"]):
                return True
            if message.attachments[0].sticker.sticker_id in self.data["mixin"]:
                return True


class MessageRule(AbstractMessageRule):
    def __init__(self, message: typing.Union[str, typing.List[str]]):
        if isinstance(message, str):
            message = [message]
        self.data = {"message": message}

    def check(self, message: Message):
        if message.text in self.data["message"]:
            return True


class EventRule(AbstractRule):
    def __init__(self, event: typing.Union[str, typing.List[str]]):
        if isinstance(event, str):
            event = [event]
        self.data = {"event": event}

    def check(self, event):
        for e in self.data["event"]:
            if "data" not in self.data:
                self.data = {"data": dict}
            if e == event:
                return True


class VBMLRule(AbstractMessageRule):
    def __init__(
        self,
        pattern: typing.Union[str, Pattern, typing.List[typing.Union[str, Pattern]]],
    ):
        self._patcher = Patcher.get_current()
        patterns: typing.List[Pattern] = []
        if isinstance(pattern, Pattern):
            patterns = [pattern]
        elif isinstance(pattern, list):
            for p in pattern:
                if isinstance(p, str):
                    patterns.append(self._patcher.pattern(p))
                else:
                    patterns.append(p)
        elif isinstance(pattern, str):
            patterns = [self._patcher.pattern(pattern)]

        self.data = {"pattern": patterns}

    def check(self, message: Message):
        patterns: typing.List[Pattern] = self.data["pattern"]

        for pattern in patterns:
            if self._patcher.check(message.text, pattern) is not None:
                self.context.kwargs = pattern.dict()
                return True


class AttachmentRule(UnionMixin):
    def check(self, message: Message):
        attachments = [
            list(attachment.dict(skip_defaults=True).keys())[0]
            for attachment in message.attachments
        ]
        if len(attachments) and not len(self.data["mixin"]):
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

    def check(self, message: Message):
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

    def check(self, message: Message):
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
