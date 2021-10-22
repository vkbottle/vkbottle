import re
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Type, Union

import vbml
from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import bot
from vkbottle.dispatch.views.bot import BotMessageView, HandlerBasement, RawBotEventView

from .abc import ABCBotLabeler

if TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.dispatch.views import ABCView
    from vkbottle.dispatch.views.bot import ABCBotMessageView

    from .abc import EventName, LabeledHandler, LabeledMessageHandler


DEFAULT_CUSTOM_RULES: Dict[str, Type["ABCRule"]] = {
    "from_chat": bot.PeerRule,
    "command": bot.CommandRule,
    "from_user": bot.FromUserRule,
    "peer_ids": bot.FromPeerRule,
    "sticker": bot.StickerRule,
    "attachment": bot.AttachmentTypeRule,
    "levenstein": bot.LevensteinRule,
    "lev": bot.LevensteinRule,
    "length": bot.MessageLengthRule,
    "action": bot.ChatActionRule,
    "payload": bot.PayloadRule,
    "payload_contains": bot.PayloadContainsRule,
    "payload_map": bot.PayloadMapRule,
    "func": bot.FuncRule,
    "coro": bot.CoroutineRule,
    "coroutine": bot.CoroutineRule,
    "state": bot.StateRule,
    "state_group": bot.StateGroupRule,
    "regexp": bot.RegexRule,
    "regex": bot.RegexRule,
    "macro": bot.MacroRule,
    "text": bot.VBMLRule,
}


class BotLabeler(ABCBotLabeler):
    """BotLabeler - shortcut manager for router
    Can be loaded to other BotLabeler
    >>> bl = BotLabeler()
    >>> ...
    >>> bl.load(BotLabeler())
    Views are fixed. Custom rules can be set locally (they are
    not inherited to other labelers). Rule config is accessible from
    all custom rules from ABCRule.config
    """

    def __init__(
        self,
        message_view: Optional["ABCBotMessageView"] = None,
        raw_event_view: Optional[RawBotEventView] = None,
        custom_rules: Optional[Dict[str, Type["ABCRule"]]] = None,
        auto_rules: Optional[List["ABCRule"]] = None,
    ):
        # Default views are fixed in BotLabeler,
        # if you need to create your own implement
        # custom labeler
        self.message_view = message_view or BotMessageView()
        self.raw_event_view = raw_event_view or RawBotEventView()

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
                    bot.PeerRule(True),
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
                    bot.PeerRule(False),
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
        event: Union["EventName", List["EventName"]],
        dataclass: Callable = dict,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledHandler":

        if not isinstance(event, list):
            event = [event]

        def decorator(func):
            for e in event:

                if isinstance(e, str):
                    e = GroupEventType(e)

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

    def load(self, labeler: "BotLabeler"):
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
