import typing
import warnings
from vkbottle.utils import logger

from vbml import Patcher

from vkbottle.framework.framework.handler.bot.events import BotEvents
from vkbottle.const import __version__
from vkbottle.framework.framework.rule.filters import AbstractFilter
from vkbottle.framework.framework.rule import (
    AbstractRule,
    ChatMessage,
    PrivateMessage,
    Any,
    AbstractMessageRule,
)

from ..handler import ABCHandler
from ..message import ABCMessageHandler


class MessageHandler(ABCMessageHandler):
    def __init__(self, *, default_rules: typing.List[AbstractMessageRule]):
        super().__init__()
        self._default_rules = default_rules
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


class BotHandler(ABCHandler):
    def __init__(self, group_id: int = 0, patcher: Patcher = Patcher()):
        self.group_id: int = group_id
        self.message_rules: typing.List[typing.List[AbstractRule]] = list()

        self.message: MessageHandler = MessageHandler(default_rules=[PrivateMessage()])
        self.chat_message: MessageHandler = MessageHandler(
            default_rules=[ChatMessage()]
        )
        self.message_handler: MessageHandler = MessageHandler(default_rules=[Any()])
        self.event: BotEvents = BotEvents()

        self._pre_p: typing.Optional[typing.Callable] = None
        self._patcher = Patcher.get_current() or patcher

    def concatenate(self, handler: "BotHandler"):
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
            self._pre_p = handler.pre_p

        logger.debug(
            "BotHandler was concatenated with {handler}",
            handler=handler.__class__.__name__,
        )

    async def dispatch(self, get_current_rest: typing.Callable = None) -> None:
        """
        Dispatch handlers from only-handlers and both-handlers
        :param get_current_rest: REST from vkbottle-rest
        :return:
        """

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
