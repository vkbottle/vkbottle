import typing
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
    FromMe,
)
from vkbottle.framework.framework.rule.filters import AbstractFilter
from vkbottle.utils.exceptions import HandlerError
from vbml import Pattern, Patcher
from .events import UserEvents, ADDITIONAL_FIELDS

COL_RULES = {
    "commands": CommandRule,
    "sticker": StickerRule,
    "levenstein": LevenshteinDisRule,
    "lev": LevenshteinDisRule,
    "from_me": FromMe,
}


class Handler:
    def __init__(self):
        self.event: UserEvents = UserEvents()
        self.message_rules: typing.List[UserLongPollEventRule] = list()

        # Main message handling managers
        self.message: MessageHandler = MessageHandler([PrivateMessage()])
        self.chat_message: MessageHandler = MessageHandler([ChatMessage()])
        self.message_handler: MessageHandler = MessageHandler()

    def dispatch(self):
        self.message_rules.extend(
            self.message.rules + self.chat_message.rules + self.message_handler.rules
        )

    def concatenate(self, other: "Handler"):
        self.event.rules += other.event.rules
        self.message.concatenate(other.message)
        self.chat_message.concatenate(other.chat_message)
        self.message_handler.concatenate(other.message_handler)


class MessageHandler:
    def __init__(self, default_rules: typing.List = None):
        self.rules: typing.List[typing.List[UserLongPollEventRule]] = list()
        self._default_rules = default_rules or []
        self._patcher = Patcher.get_current()
        self.prefix: list = ["/", "!"]

    def add_handled_rule(
        self, rules: typing.List[AbstractRule], func: typing.Callable
    ) -> UserLongPollEventRule:
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

    def add_rules(
        self, rules: typing.List[AbstractRule], func: typing.Callable
    ) -> UserLongPollEventRule:
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
