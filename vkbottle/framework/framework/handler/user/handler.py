import typing
from vkbottle.types.user_longpoll import Message
from vkbottle.framework.framework.rule import (
    AbstractRule,
    VBMLRule,
    UserLongPollEventRule,
    PrivateMessage,
    ChatMessage,
    AbstractMessageRule,
    Any,
)
from vkbottle.framework.framework.rule.filters import AbstractFilter
from vkbottle.utils.logger import logger
from vkbottle.const import __version__
from vbml import Patcher
from .events import UserEvents, ADDITIONAL_FIELDS
from ..handler import ABCHandler
from ..message import ABCMessageHandler


class MessageHandler(ABCMessageHandler):
    def __init__(self, *, default_rules: typing.List[AbstractMessageRule]):
        super().__init__()
        self._default_rules = default_rules
        self._patcher = Patcher.get_current()

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
        self.rules.append([rule])
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


class UserHandler(ABCHandler):
    def __init__(self):
        self.event: UserEvents = UserEvents()
        self.message_rules: typing.List[UserLongPollEventRule] = list()

        # Main message handling managers
        self.message: MessageHandler = MessageHandler(default_rules=[PrivateMessage()])
        self.chat_message: MessageHandler = MessageHandler(
            default_rules=[ChatMessage()]
        )
        self.message_handler: MessageHandler = MessageHandler(default_rules=[Any()])

    async def dispatch(
        self, get_current_rest: typing.Callable[[], typing.Awaitable[dict]] = None
    ) -> None:
        self.message_handler.rules += self.message.rules + self.chat_message.rules
        self.message_rules += self.message_handler.rules

        if get_current_rest:
            # Check updates from timoniq/vkbottle-rest
            current_rest = await get_current_rest()
            if current_rest.get("version") != __version__:
                logger.info(
                    "You are using old version of VKBottle. Update is found: {} | {}",
                    current_rest.get("version"),
                    current_rest.get("description"),
                )
        logger.debug("Bot was successfully dispatched")

    def concatenate(self, other: "UserHandler"):
        self.event.rules += other.event.rules
        self.message.concatenate(other.message)
        self.chat_message.concatenate(other.chat_message)
        self.message_handler.concatenate(other.message_handler)
