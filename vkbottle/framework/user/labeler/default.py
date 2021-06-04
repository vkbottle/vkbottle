import re
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union

import vbml

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule, user
from vkbottle.dispatch.views import ABCView
from vkbottle.dispatch.views.user import HandlerBasement, RawUserEventView, UserMessageView
from vkbottle.tools.dev.utils import convert_shorten_filter

from .abc import ABCUserLabeler, LabeledHandler, LabeledMessageHandler

ShortenRule = Union[ABCRule, Tuple[ABCRule, ...], Set[ABCRule]]
DEFAULT_CUSTOM_RULES: Dict[str, Type[ABCRule]] = {
    "from_chat": user.PeerRule,
    "command": user.CommandRule,
    "from_user": user.FromUserRule,
    "peer_ids": user.FromPeerRule,
    "sticker": user.StickerRule,
    "attachment": user.AttachmentTypeRule,
    "levenstein": user.LevensteinRule,
    "lev": user.LevensteinRule,
    "length": user.MessageLengthRule,
    "action": user.ChatActionRule,
    "func": user.FuncRule,
    "coro": user.CoroutineRule,
    "coroutine": user.CoroutineRule,
    "state": user.StateRule,
    "state_group": user.StateGroupRule,
    "regexp": user.RegexRule,
    "macro": user.MacroRule,
    "text": user.VBMLRule,
}


class UserLabeler(ABCUserLabeler):
    """UserLabeler - shortcut manager for router
    Can be loaded to other UserLabeler
    >>> bl = UserLabeler()
    >>> ...
    >>> bl.load(UserLabeler())
    Views are fixed. Custom rules can be set locally (they are
    not inherited to other labelers). Rule config is accessible from
    all custom rules from ABCRule.config
    """

    def __init__(self, **kwargs):
        # Default views are fixed in UserLabeler,
        # if you need to create your own implement
        # custom labeler
        self.message_view = UserMessageView()
        self.raw_event_view = RawUserEventView()

        self.custom_rules = kwargs.get("custom_rules") or DEFAULT_CUSTOM_RULES
        self.auto_rules: List["ABCRule"] = []

        # Rule config is accessible from every single custom rule
        self.rule_config: Dict[str, Any] = {
            "vbml_flags": re.MULTILINE,  # Flags for VBMLRule
            "vbml_patcher": vbml.Patcher(),  # Patcher for VBMLRule
        }

    @property
    def vbml_ignore_case(self) -> bool:
        """Gets ignore case flag from rule config flags"""
        return re.IGNORECASE in self.rule_config["flags"]

    @vbml_ignore_case.setter
    def vbml_ignore_case(self, ignore_case: bool):
        """Adds ignore case flag to rule config flags or removes it"""
        if not ignore_case:
            self.rule_config["vbml_flags"] ^= re.IGNORECASE
        else:
            self.rule_config["vbml_flags"] |= re.IGNORECASE

    @property
    def vbml_patcher(self) -> vbml.Patcher:
        return self.rule_config["vbml_patcher"]

    @vbml_patcher.setter
    def vbml_patcher(self, patcher: vbml.Patcher):
        self.rule_config["vbml_patcher"] = patcher

    @property
    def vbml_flags(self) -> re.RegexFlag:
        return self.rule_config["vbml_flags"]

    @vbml_flags.setter
    def vbml_flags(self, flags: re.RegexFlag):
        self.rule_config["vbml_flags"] = flags

    def message(
        self, *rules: ShortenRule, blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    *map(convert_shorten_filter, rules),
                    *self.auto_rules,
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
                    user.PeerRule(True),
                    *map(convert_shorten_filter, rules),
                    *self.auto_rules,
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
                    user.PeerRule(False),
                    *map(convert_shorten_filter, rules),
                    *self.auto_rules,
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
                        *self.auto_rules,
                        *self.get_custom_rules(custom_rules),
                    ),
                )
            return func

        return decorator

    def load(self, labeler: "UserLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.update(labeler.message_view.middlewares)
        self.raw_event_view.handlers.update(labeler.raw_event_view.handlers)
        self.raw_event_view.middlewares.update(labeler.raw_event_view.middlewares)

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k].with_config(self.rule_config)(v) for k, v in custom_rules.items()]  # type: ignore

    def views(self) -> Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_event_view}
