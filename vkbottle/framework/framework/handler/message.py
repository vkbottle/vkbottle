import re
import typing
from abc import ABC, abstractmethod

from vbml import Pattern, Patcher

from vkbottle.framework.framework.rule import (
    AbstractRule,
    VBMLRule,
    CommandRule,
    StickerRule,
    LevenshteinDisRule,
    PayloadRule,
    FromMe,
)
from vkbottle.utils.exceptions import HandlerError

COL_RULES = {
    "commands": CommandRule,
    "sticker": StickerRule,
    "levenstein": LevenshteinDisRule,
    "lev": LevenshteinDisRule,
    "payload": PayloadRule,
    "from_me": FromMe,
}


class ABCMessageHandler(ABC):

    _patcher: Patcher

    def __init__(self):
        self.rules: typing.List[typing.List[AbstractRule]] = []
        self.prefix: typing.List[typing.AnyStr] = []
        self._default_rules: typing.List[AbstractRule] = []

    @abstractmethod
    def add_rules(self, rules: typing.List[AbstractRule], func: typing.Callable):
        pass

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

        return rule

    def concatenate(self, message_handler: "ABCMessageHandler"):
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
        current: typing.List[AbstractRule] = []

        if text:
            current.append(
                self._text_rule(func, text, lower, command, pattern or "{}$")
            )

        current.extend(rules)
        current.extend(self._col_rules(**col_rules))

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
            current: typing.List[AbstractRule] = []

            if text:
                current.append(self._text_rule(func, text, lower, command, "{}$"))

            current.extend(rules)
            current.extend(self._col_rules(**col_rules))

            self.add_rules(current, func)
            return func

        return decorator

    def __repr__(self):
        rules = ""
        for rule in self.rules:
            rules += (
                "("
                + rule[0].call.__name__
                + ": "
                + ", ".join([rule_.__class__.__name__ for rule_ in rule])
                + "), "
            )
        return "<ABCMessageHandler {}>".format(rules.rstrip(", "))

    def __bool__(self):
        return len(self.rules) > 0

    @property
    def default_rules(self):
        return [r.copy() for r in self._default_rules]
