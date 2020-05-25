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
    StickerRule,
    AbstractMessageRule,
)

COL_RULES = {
    "commands": CommandRule,
    "sticker": StickerRule,
}


class Handler:
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
        )
        self.message_rules += self.message_handler.rules

        if get_current_rest:

            # Check updates from timoniq/vkbottle-rest
            current_rest = await get_current_rest()
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
                    current_rest.get("version"),
                    current_rest.get("description"),
                )
        logger.debug("Bot was successfully dispatched")
