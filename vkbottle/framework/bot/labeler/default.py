from typing import Dict, Union, List, Callable, Tuple, Set, Any, Type

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views import MessageView, ABCView, RawEventView, HandlerBasement
from vkbottle.tools.dev_tools.utils import convert_shorten_filter
from .abc import ABCBotLabeler, LabeledMessageHandler, LabeledHandler

from vkbottle.dispatch.rules.bot import (
    PeerRule,
    VBMLRule,
    CommandRule,
    FromUserRule,
    FromPeerRule,
    StickerRule,
    AttachmentTypeRule,
    LevensteinRule,
    MessageLengthRule,
    ChatActionRule,
    PayloadRule,
    PayloadContainsRule,
    PayloadMapRule,
    FuncRule,
    CoroutineRule,
    StateRule,
    RegexRule,
)

import re
import vbml


ShortenRule = Union[ABCRule, Tuple[ABCRule, ...], Set[ABCRule]]
DEFAULT_CUSTOM_RULES: Dict[str, Type[ABCRule]] = {
    "from_chat": PeerRule,
    "command": CommandRule,
    "from_user": FromUserRule,
    "peer_ids": FromPeerRule,
    "sticker": StickerRule,
    "attachment": AttachmentTypeRule,
    "levenstein": LevensteinRule,
    "lev": LevensteinRule,
    "length": MessageLengthRule,
    "action": ChatActionRule,
    "payload": PayloadRule,
    "payload_contains": PayloadContainsRule,
    "payload_map": PayloadMapRule,
    "func": FuncRule,
    "coro": CoroutineRule,
    "coroutine": CoroutineRule,
    "state": StateRule,
    "regexp": RegexRule,
}


class BotLabeler(ABCBotLabeler):
    def __init__(self, **kwargs):
        self.message_view = MessageView()
        self.raw_event_view = RawEventView()
        self.patcher = kwargs.get("patcher") or vbml.Patcher()
        self.custom_rules = kwargs.get("custom_rules") or DEFAULT_CUSTOM_RULES
        self.custom_rules["text"] = lambda x: self.get_vbml_rule(self, x)
        self.ignore_case = False
        self.default_flags = re.MULTILINE

    def message(
        self, *rules: ShortenRule, blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    *map(convert_shorten_filter, rules),
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def chat_message(
        self, *rules: ShortenRule, blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    PeerRule(True),
                    *map(convert_shorten_filter, rules),
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def private_message(
        self, *rules: ShortenRule, blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    PeerRule(False),
                    *map(convert_shorten_filter, rules),
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def raw_event(
        self,
        event: Union[str, List[str]],
        dataclass: Callable = dict,
        *rules: ShortenRule,
        **custom_rules,
    ) -> LabeledHandler:
        if not isinstance(event, list):
            event = [event]

        def decorator(func):
            for e in event:
                self.raw_event_view.handlers[e] = HandlerBasement(
                    dataclass,
                    FromFuncHandler(
                        func,
                        *map(convert_shorten_filter, rules),
                        *self.get_custom_rules(custom_rules),
                    ),
                )
            return func

        return decorator

    def load(self, labeler: "BotLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.extend(labeler.message_view.middlewares)
        self.raw_event_view.handlers.update(labeler.raw_event_view.handlers)
        self.raw_event_view.middlewares.extend(labeler.raw_event_view.middlewares)

    @staticmethod
    def get_vbml_rule(labeler: "BotLabeler", pattern: Any) -> "VBMLRule":
        """ Cast a vbml rule with patcher and flags, needed to simplify
        VBMLRule setup.
        """
        return VBMLRule(
            pattern,
            labeler.patcher,
            flags=(
                labeler.default_flags if not labeler.ignore_case else re.MULTILINE | re.IGNORECASE
            ),
        )

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k](v) for k, v in custom_rules.items()]  # type: ignore

    def views(self) -> Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_event_view}
