import typing
import warnings
import re
from vkbottle.types.user_longpoll import Message
from vkbottle.framework.framework.rule import (
    AbstractRule,
    VBMLRule,
    UserLongPollEventRule,
    CommandRule,
    StickerRule,
    LevenshteinDisRule,
    PrivateMessage,
    ChatMessage,
)
from vkbottle.framework.framework.rule.filters import AbstractFilter
from vkbottle.api.exceptions import HandlerError
from vbml import Pattern, Patcher

ADDITIONAL_FIELDS = ("peer_id", "timestamp", "text", "info", "attachments", "random_id")
COL_RULES = {
    "commands": CommandRule,
    "sticker": StickerRule,
    "levenstein": LevenshteinDisRule,
    "lev": LevenshteinDisRule,
}


class Handler:
    def __init__(self):
        self.rules: typing.List[UserLongPollEventRule] = list()

        # Main message handling managers
        self.message: MessageHandler = MessageHandler([PrivateMessage()])
        self.chat_message: MessageHandler = MessageHandler([ChatMessage()])
        self.message_handler: MessageHandler = MessageHandler()

    def dispatch(self):
        self.rules.extend(
            self.message.rules
            + self.chat_message.rules
            + self.message_handler.rules
        )

    def message_new(self, *rules: typing.Tuple[typing.Union[AbstractRule, AbstractFilter]]):
        warnings.warn(
            "Event message_new is deprecated, use message, chat_message, message_handler instead. See issue #77",
            DeprecationWarning
        )

        def decorator(func):
            rule = UserLongPollEventRule(4, *rules)
            rule.create(
                func,
                {
                    "name": "message_new",
                    "data": ["message_id", "flags", *ADDITIONAL_FIELDS],
                    "dataclass": Message,
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def concatenate(self, other: "Handler"):
        self.rules += other.rules

    def message_flag_change(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(1, *rules)
            rule.create(
                func,
                {
                    "name": "message_flag_change",
                    "data": ["message_id", "flags", *ADDITIONAL_FIELDS],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_flag_set(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(2, *rules)
            rule.create(
                func,
                {
                    "name": "message_flag_set",
                    "data": ["message_id", "mask", *ADDITIONAL_FIELDS],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_flag_remove(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(3, *rules)
            rule.create(
                func,
                {
                    "name": "message_flag_remove",
                    "data": ["message_id", "mask", *ADDITIONAL_FIELDS],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_edit(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(5, *rules)
            rule.create(
                func,
                {
                    "name": "message_edit",
                    "data": [
                        "message_id",
                        "mask",
                        "peer_id",
                        "timestamp",
                        "new_text",
                        *ADDITIONAL_FIELDS,
                    ],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_read_in(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(6, *rules)
            rule.create(
                func, {"name": "message_read_in", "data": ["peer_id", "local_id"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_read_out(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(7, *rules)
            rule.create(
                func, {"name": "message_read_out", "data": ["peer_id", "local_id"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def friend_online(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(8, *rules)
            rule.create(
                func,
                {"name": "friend_online", "data": ["user_id", "extra", "timestamp"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def friend_offline(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(9, *rules)
            rule.create(
                func,
                {"name": "friend_offline", "data": ["user_id", "flags", "timestamp"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_flag_change(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(11, *rules)
            rule.create(
                func, {"name": "chat_flag_change", "data": ["peer_id", "flags"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_flag_set(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(12, *rules)
            rule.create(
                func, {"name": "chat_flag_set", "data": ["peer_id", "mask"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_flag_remove(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(10, *rules)
            rule.create(
                func, {"name": "chat_flag_remove", "data": ["peer_id", "mask"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_remove(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(13, *rules)
            rule.create(
                func, {"name": "chat_remove", "data": ["peer_id", "local_id"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_restore(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(14, *rules)
            rule.create(
                func, {"name": "chat_restore", "data": ["peer_id", "local_id"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_edit(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(51, *rules)
            rule.create(
                func, {"name": "chat_edit", "data": ["chat_id", "self"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_info_edit(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(52, *rules)
            rule.create(
                func,
                {"name": "chat_info_edit", "data": ["type_id", "peer_id", "info"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_typing_state(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(61, *rules)
            rule.create(
                func, {"name": "message_typing_state", "data": ["user_id", "flags"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_typing_state(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(62, *rules)
            rule.create(
                func, {"name": "chat_typing_state", "data": ["user_id", "chat_id"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_typing_states(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(63, *rules)
            rule.create(
                func,
                {
                    "name": "chat_typing_states",
                    "data": ["user_ids", "peer_id", "total_count", "ts",],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_voice_message_states(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(64, *rules)
            rule.create(
                func,
                {
                    "name": "chat_voice_message_states",
                    "data": ["user_ids", "peer_id", "total_count", "ts",],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def call(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(70, *rules)
            rule.create(
                func, {"name": "call", "data": ["user_id", "call_id"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def left_counter(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(80, *rules)
            rule.create(
                func, {"name": "left_counter", "data": ["counter", "null"]},
            )
            self.rules.append(rule)
            return func

        return decorator

    def notifications_settings_changed(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(114, *rules)
            rule.create(
                func,
                {
                    "name": "notifications_settings_changed",
                    "data": ["peer_id", "sound", "disabled_until",],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def __repr__(self):
        return "<user.Handler>"


class MessageHandler:
    def __init__(self, default_rules: typing.List = None):
        self.rules: typing.List[typing.List[UserLongPollEventRule]] = list()
        self._default_rules = default_rules or []
        self._patcher = Patcher.get_current()
        self.prefix: list = ["/", "!"]

    def add_handled_rule(self, rules: typing.List[AbstractRule], func: typing.Callable) -> UserLongPollEventRule:
        rule = UserLongPollEventRule(4, *rules)
        rule.create(
            func,
            {
                "name": "message_new",
                "data": ["message_id", "flags", *ADDITIONAL_FIELDS],
                "dataclass": Message,
            },
        )
        self.rules.append(rule)
        return rule

    def add_rules(self, rules: typing.List[AbstractRule], func: typing.Callable) -> UserLongPollEventRule:
        current = list()
        for rule in self.default_rules + rules:
            if isinstance(rule, str):
                rule = VBMLRule(rule)
            if not isinstance(rule, AbstractFilter):
                rule.create(func)
            current.append(rule)
        return self.add_handled_rule(current, func)

    def _col_rules(self, **col) -> typing.List[AbstractRule]:
        current = list()
        for k, v in col.items():
            if k not in COL_RULES:
                raise HandlerError("Col Rule {} is undefined".format(k))
            current.append(COL_RULES[k](v))
        return current

    def _text_rule(
        self,
        func: typing.Callable,
        text: typing.Union[str, Pattern, typing.List[typing.Union[str, Pattern]]],
        lower: bool,
        command: bool,
        pattern: str,
    ) -> AbstractRule:
        source = None

        if not isinstance(text, dict):
            texts: typing.List[typing.Union[str, Pattern]] = text if isinstance(
                text, list
            ) else [text]
        else:
            source = list(text.values())
            texts = list(text.keys())

        patterns: typing.List[Pattern] = []

        for text in texts:
            if not isinstance(text, Pattern):
                prefix = ("[" + "|".join(self.prefix) + "]") if command else ""
                patterns.append(
                    self._patcher.pattern(
                        text,
                        pattern=(prefix + pattern) if prefix else pattern,
                        flags=re.IGNORECASE if lower else None,
                    )
                )
            else:
                patterns.append(text)

        rule = VBMLRule(patterns)
        if source:
            rule.watch_context = dict(zip(patterns, source))
        arguments = [
            arguments for pattern in patterns for arguments in pattern.arguments
        ]

        return rule

    def concatenate(self, message_handler: "MessageHandler"):
        self.rules += message_handler.rules
        self.prefix += [p for p in message_handler.prefix if p not in self.prefix]

    def add_handler(
        self,
        func: typing.Callable,
        *rules,
        text: typing.Union[
            str, Pattern, typing.List[typing.Union[str, Pattern]]
        ] = None,
        lower: bool = False,
        command: bool = False,
        pattern: str = None,
        **col_rules,
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
        current: typing.List[AbstractRule] = list(rules)
        current.extend(self._col_rules(**col_rules))

        if text:
            current.append(
                self._text_rule(func, text, lower, command, pattern or "{}$")
            )

        self.add_rules(current, func)

    def rule(self, *rules):
        def decorator(func):
            current: typing.List[AbstractRule] = list()

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.add_rules(current, func)
            return func

        return decorator

    def __call__(
        self,
        *rules,
        text: typing.Union[
            str, Pattern, typing.List[typing.Union[str, Pattern]]
        ] = None,
        command: bool = False,
        lower: bool = False,
        **col_rules,
    ):
        """
        Simple on.message(text) decorator. Support regex keys in text
        :param text: text (match case)
        :param command: Is this is a /command
        :param lower: Should IGNORECASE param for regex be used
        """

        def decorator(func):
            current: typing.List[AbstractRule] = list(rules)
            current.extend(self._col_rules(**col_rules))

            if text:
                current.append(self._text_rule(func, text, lower, command, "{}$"))

            self.add_rules(current, func)
            return func

        return decorator

    def __repr__(self):
        rules = ""
        for rules in self.rules:
            rules += (
                rules[0].call.__name__
                + ": "
                + ", ".join([rule.__class__.__name__ for rule in rules])
                + "\n"
            )
        return rules

    def __bool__(self):
        return len(self.rules) > 0

    @property
    def default_rules(self):
        return [r.copy() for r in self._default_rules]
