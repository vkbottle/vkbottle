import re
from typing import Dict, Union, List, Callable, Tuple, Set, Any, Type

import vbml

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule
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
from vkbottle.dispatch.views import MessageView, ABCView, RawEventView, HandlerBasement
from vkbottle.tools.dev_tools.utils import convert_shorten_filter
from .abc import ABCBotLabeler, LabeledMessageHandler, LabeledHandler

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
    "text": VBMLRule,
}


class BotLabeler(ABCBotLabeler):
    """ BotLabeler - shortcut manager for router
    Can be loaded to other BotLabeler
    >>> bl = BotLabeler()
    >>> ...
    >>> bl.load(BotLabeler())
    Views are fixed. Custom rules can be set locally (they are
    not inherited to other labelers). Rule config is accessible from
    all custom rules from ABCRule.config
    """

    def __init__(self, **kwargs):
        # Default views are fixed in BotLabeler,
        # if you need to create your own implement
        # custom labeler
        self.message_view = MessageView()
        self.raw_event_view = RawEventView()

        self.custom_rules = kwargs.get("custom_rules") or DEFAULT_CUSTOM_RULES

        # Rule config is accessible from every single custom rule
        self.rule_config: Dict[str, Any] = {
            "vbml_flags": re.MULTILINE,  # Flags for VBMLRule
            "vbml_patcher": vbml.Patcher(),  # Patcher for VBMLRule
        }

    @property
    def vbml_ignore_case(self) -> bool:
        """ Gets ignore case flag from rule config flags """
        return re.IGNORECASE in self.rule_config["flags"]

    @vbml_ignore_case.setter
    def vbml_ignore_case(self, ignore_case: bool):
        """ Adds ignore case flag to rule config flags or removes it
        """
        if not ignore_case:
            self.rule_config["flags"] ^= re.IGNORECASE
        else:
            self.rule_config["flags"] |= re.IGNORECASE

    @property
    def vbml_patcher(self) -> vbml.Patcher:
        return self.rule_config["patcher"]

    @vbml_patcher.setter
    def vbml_patcher(self, patcher: vbml.Patcher):
        self.rule_config["patcher"] = patcher

    @property
    def vbml_flags(self) -> re.RegexFlag:
        return self.rule_config["flags"]

    @vbml_flags.setter
    def vbml_flags(self, flags: re.RegexFlag):
        self.rule_config["flags"] = flags

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

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k].with_config(self.rule_config)(v) for k, v in custom_rules.items()]  # type: ignore

    def views(self) -> Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_event_view}
