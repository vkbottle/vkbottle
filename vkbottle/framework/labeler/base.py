import re

import typing_extensions as typing
import vbml

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule, base

from .abc import ABCLabeler

if typing.TYPE_CHECKING:
    from vkbottle.dispatch.views import ABCView
    from vkbottle.dispatch.views.abc import ABCMessageView, ABCRawEventView

    from .abc import LabeledMessageHandler

CustomRuleType = typing.Dict[str, typing.Type["ABCRule"]]

DEFAULT_CUSTOM_RULES: CustomRuleType = {
    "from_chat": base.PeerRule,
    "mention": base.MentionRule,
    "command": base.CommandRule,
    "from_user": base.FromUserRule,
    "peer_ids": base.FromPeerRule,
    "sticker": base.StickerRule,
    "attachment": base.AttachmentTypeRule,
    "levenshtein": base.LevenshteinRule,
    "lev": base.LevenshteinRule,
    "length": base.MessageLengthRule,
    "action": base.ChatActionRule,
    "payload": base.PayloadRule,
    "payload_contains": base.PayloadContainsRule,
    "payload_map": base.PayloadMapRule,
    "func": base.FuncRule,
    "coro": base.CoroutineRule,
    "coroutine": base.CoroutineRule,
    "state": base.StateRule,
    "state_group": base.StateGroupRule,
    "regexp": base.RegexRule,
    "regex": base.RegexRule,
    "reply_message": base.ReplyMessageRule,
    "macro": base.MacroRule,
    "text": base.VBMLRule,
    "fuzzy": base.FuzzyTextRule,
    "is_admin": base.IsAdminRule,
}


class BaseLabeler(ABCLabeler):
    def __init__(
        self,
        message_view: "ABCMessageView",
        raw_event_view: "ABCRawEventView",
        custom_rules: typing.Optional[CustomRuleType] = None,
        auto_rules: typing.Optional[typing.List["ABCRule"]] = None,
        raw_event_auto_rules: typing.Optional[typing.List["ABCRule"]] = None,
    ) -> None:
        self.message_view = message_view
        self.raw_event_view = raw_event_view

        self.custom_rules = custom_rules or DEFAULT_CUSTOM_RULES
        self.auto_rules = auto_rules or []
        self.raw_event_auto_rules = raw_event_auto_rules or []

        # Rule config is accessible from every single custom rule
        self.rule_config: typing.Dict[str, typing.Any] = {
            "vbml_flags": re.DOTALL,  # Flags for VBMLRule
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
        self,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledMessageHandler":
        if any(not isinstance(rule, ABCRule) for rule in rules):
            msg = "All rules must be subclasses of ABCRule or rule shortcuts (https://vkbottle.rtfd.io/ru/latest/high-level/handling/rules/)"
            raise ValueError(msg)

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
        self,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledMessageHandler":
        if any(not isinstance(rule, ABCRule) for rule in rules):
            msg = "All rules must be subclasses of ABCRule or rule shortcuts (https://vkbottle.rtfd.io/ru/latest/high-level/handling/rules/)"
            raise ValueError(msg)

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
        self,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledMessageHandler":
        if any(not isinstance(rule, ABCRule) for rule in rules):
            msg = "All rules must be subclasses of ABCRule or rule shortcuts (https://vkbottle.rtfd.io/ru/latest/high-level/handling/rules/)"
            raise ValueError(msg)

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

    def load(self, labeler: "BaseLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.extend(labeler.message_view.middlewares)
        self.raw_event_view.middlewares.extend(labeler.raw_event_view.middlewares)
        for event, handler_basements in labeler.raw_event_view.handlers.items():
            event_handlers = self.raw_event_view.handlers.setdefault(event, [])
            event_handlers.extend(handler_basements)

    def get_custom_rules(
        self,
        custom_rules: typing.Dict[str, typing.Any],
    ) -> typing.List["ABCRule"]:
        return [
            self.custom_rules[k].with_config(self.rule_config)(v)  # type: ignore
            for k, v in custom_rules.items()  # type: ignore
        ]

    def views(self) -> typing.Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_event_view}
