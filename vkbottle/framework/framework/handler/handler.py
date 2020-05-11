import typing
import warnings
import re
from vkbottle.utils import logger

from vbml import Patcher, Pattern

from .events import Event
from vkbottle.const import __version__
from vkbottle.utils.exceptions import HandlerError
from vkbottle.framework.framework.rule.filters import AbstractFilter
from vkbottle.framework.framework.rule import (
    AbstractRule,
    VBMLRule,
    ChatActionRule,
    PayloadRule,
    ChatMessage,
    PrivateMessage,
    Any,
    CommandRule,
    StickerRule,
    LevenshteinDisRule,
)

COL_RULES = {
    "commands": CommandRule,
    "sticker": StickerRule,
    "levenstein": LevenshteinDisRule,
    "lev": LevenshteinDisRule,
}


class Handler:
    def __init__(self, group_id: int = 0, patcher: Patcher = Patcher()):
        self.group_id: int = group_id
        self.rules: typing.List[typing.List[AbstractRule]] = list()

        self.message: MessageHandler = MessageHandler(default_rules=[PrivateMessage()])
        self.chat_message: MessageHandler = MessageHandler(
            default_rules=[ChatMessage()]
        )
        self.message_handler: MessageHandler = MessageHandler(default_rules=[Any()])
        self.event: Event = Event()

        self._pre_p: typing.Optional[typing.Callable] = None
        self._patcher = Patcher.get_current() or patcher

        if not hasattr(Pattern, "context_copy"):
            raise RuntimeError(
                "\n\n\tNow! Update vbml with command:\n"
                "\tpip install https://github.com/timoniq/vbml/archive/master.zip --upgrade\n"
                "\ttnx <3"
            )

    def concatenate(self, handler: "Handler"):
        """
        Concatenate handlers from current handler and another handler
        :param handler: another handler
        :return:
        """
        self.message.concatenate(handler.message)
        self.chat_message.concatenate(handler.chat_message)
        self.message_handler.concatenate(handler.message_handler)
        self.event.rules += handler.event.rules
        if not self._pre_p:
            self._pre_p = handler.pre

        logger.debug(
            "Bot Handler was concatenated with {handler}",
            handler=handler.__class__.__name__,
        )

    async def dispatch(self, get_current_rest: typing.Callable = None) -> None:
        """
        Dispatch handlers from only-handlers and both-handlers
        :param get_current_rest: REST from vkbottle-rest
        :return:
        """

        self.message_handler.rules += self.message.rules + self.chat_message.rules
        self.message_handler.payload.rules += (
            self.message.payload.rules + self.chat_message.payload.rules
        )

        self.rules = self.message_handler.payload.rules + self.message_handler.rules

        if get_current_rest:

            # Check updates from timoniq/vkbottle-rest
            current_rest = await get_current_rest()
            if current_rest["version"] != __version__:
                logger.info(
                    "You are using old version of VKBottle. Update is found: {} | {}",
                    current_rest["version"],
                    current_rest["description"],
                )
        logger.debug("Bot successfully dispatched")

    def change_prefix_for_all(self, prefix: list) -> None:
        self.message.prefix = prefix
        self.chat_message.prefix = prefix
        self.message_handler.prefix = prefix

    def chat_action(
        self, type_: typing.Union[str, typing.List[str]], rules: dict = None
    ):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """

        def decorator(func):
            rule = ChatActionRule(type_, rules=rules)
            self.chat_message.add_rules([rule], func)
            return func

        return decorator

    def chat_mention(self):
        def decorator(func):
            pattern = Pattern(pattern=r"\[(club|public){}\|.*?]".format(self.group_id))
            rule = VBMLRule(pattern)
            self.chat_message.add_rules([rule], func)
            return func

        return decorator

    def chat_invite(self):
        def decorator(func):
            rule = ChatActionRule("chat_invite_user", {"member_id": -self.group_id})
            self.chat_message.add_rules([rule], func)
            return func

        return decorator

    @property
    def pre(self):
        return self._pre_p

    def pre_process(self):
        def decorator(func):
            self._pre_p = func
            return func

        return decorator

    def __repr__(self):
        return (
            f"MESSAGE HANDLERS:              {len(self.message.rules) + len(self.message_handler.rules)}\n"
            f"CHAT-MESSAGE HANDLERS:         {len(self.chat_message.rules) + len(self.message_handler.rules)}\n"
            f"EVENT HANDLERS:                {len(self.event.rules)}\n"
            f"MESSAGE-PAYLOAD HANDLERS:      {len(self.message.payload.rules) + len(self.message_handler.payload.rules)}\n"
            f"CHAT-MESSAGE-PAYLOAD HANDLERS: {len(self.chat_message.payload.rules) + len(self.message_handler.payload.rules)}"
        )

    def __str__(self):
        return self.__repr__()


class MessageHandler:
    def __init__(self, default_rules: typing.List = None):
        self.payload: PayloadHandler = PayloadHandler()
        self.rules: typing.List[typing.List[AbstractRule]] = list()
        self._default_rules = default_rules or []
        self.prefix: list = ["/", "!"]
        self._patcher = Patcher.get_current()

    def add_rules(self, rules: typing.List[AbstractRule], func: typing.Callable):
        current = list()
        for rule in self.default_rules + rules:
            if not isinstance(rule, (AbstractRule, AbstractFilter)):
                warnings.warn(
                    f"Wrong rule! Got type {rule.__class__} instead of AbstractRule. Rule will be ignored",
                    Warning,
                )
                continue
            if not isinstance(rule, AbstractFilter):
                rule.create(func)
            current.append(rule)

        self.rules.append(current)

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

    def concatenate_payload(self):
        self.rules = self.payload.rules + self.rules

    def concatenate(self, message_handler: "MessageHandler"):
        self.concatenate_payload()
        self.rules += message_handler.rules
        self.prefix += [p for p in message_handler.prefix if p not in self.prefix]
        self.payload.rules += message_handler.payload.rules

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


class PayloadHandler:
    def __init__(self):
        self.rules: typing.List[typing.List[AbstractRule]] = list()

    def __call__(self, payload: dict, *rules):
        def decorator(func):
            current = list()

            rule = PayloadRule(payload, mode=1)
            rule.create(func)
            rule.data["ignore_ans"] = False
            current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)

            return func

        return decorator

    def contains(self, payload: dict, *rules):
        def decorator(func):
            current = list()

            rule = PayloadRule(payload, mode=2)
            rule.create(func)
            rule.data["ignore_ans"] = False
            current.append(rule)

            for rule in rules:
                rule.create(func)
                current.append(rule)

            self.rules.append(current)

            return func

        return decorator
