import re
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Type, Union

import vbml
from vkbottle_types.events.user_events import RawUserEvent

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import base
from vkbottle.dispatch.views.user import HandlerBasement, RawUserEventView, UserMessageView

from .abc import ABCUserLabeler

if TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.dispatch.views import ABCView
    from vkbottle.dispatch.views.user import ABCUserMessageView

    from .abc import LabeledHandler, LabeledMessageHandler


DEFAULT_CUSTOM_RULES: Dict[str, Type["ABCRule"]] = {
    "from_chat": base.PeerRule,
    "command": base.CommandRule,
    "from_user": base.FromUserRule,
    "peer_ids": base.FromPeerRule,
    "sticker": base.StickerRule,
    "attachment": base.AttachmentTypeRule,
    "levenshtein": base.LevenshteinRule,
    "lev": base.LevenshteinRule,
    "length": base.MessageLengthRule,
    "action": base.ChatActionRule,
    "func": base.FuncRule,
    "coro": base.CoroutineRule,
    "coroutine": base.CoroutineRule,
    "state": base.StateRule,
    "state_group": base.StateGroupRule,
    "regexp": base.RegexRule,
    "regex": base.RegexRule,
    "macro": base.MacroRule,
    "text": base.VBMLRule,
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

    def __init__(
        self,
        message_view: Optional["ABCUserMessageView"] = None,
        raw_event_view: Optional[RawUserEventView] = None,
        custom_rules: Optional[Dict[str, Type["ABCRule"]]] = None,
        auto_rules: Optional[List["ABCRule"]] = None,
    ):
        # Default views are fixed in UserLabeler,
        # if you need to create your own implement
        # custom labeler
        self.message_view = message_view or UserMessageView()
        self.raw_event_view = raw_event_view or RawUserEventView()

        self.custom_rules = custom_rules or DEFAULT_CUSTOM_RULES
        self.auto_rules = auto_rules or []

        # Rule config is accessible from every single custom rule
        self.rule_config: Dict[str, Any] = {
            "vbml_flags": re.MULTILINE | re.DOTALL,  # Flags for VBMLRule
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
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    *rules,
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def chat_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    base.PeerRule(),
                    *rules,
                    *self.auto_rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def private_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    base.PeerRule(False),
                    *rules,
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
        dataclass: Callable = RawUserEvent,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledHandler":

        if not isinstance(event, list):
            event = [event]

        def decorator(func):
            for e in event:
                event_handlers = self.raw_event_view.handlers.get(e)
                handler_basement = HandlerBasement(
                    dataclass,
                    FromFuncHandler(
                        func,
                        *rules,
                        *self.auto_rules,
                        *self.get_custom_rules(custom_rules),
                        blocking=blocking,
                    ),
                )
                if not event_handlers:
                    self.raw_event_view.handlers[e] = [handler_basement]
                else:
                    self.raw_event_view.handlers[e].append(handler_basement)
            return func

        return decorator

    def load(self, labeler: "UserLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.update(labeler.message_view.middlewares)
        for event, handler_basements in labeler.raw_event_view.handlers.items():
            event_handlers = self.raw_event_view.handlers.get(event)
            if event_handlers:
                event_handlers.extend(handler_basements)
            else:
                self.raw_event_view.handlers[event] = handler_basements
        self.raw_event_view.middlewares.update(labeler.raw_event_view.middlewares)

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k].with_config(self.rule_config)(v) for k, v in custom_rules.items()]  # type: ignore

    def views(self) -> Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_event_view}
