from .dispatch.rules import base as rules
from .dispatch.views import bot as views
from .framework.bot import ABCBotLabeler, Bot, BotBlueprint, BotLabeler, run_multibot
from .tools.dev.mini_types.bot import MessageEventMin, MessageMin

Message = MessageMin
MessageEvent = MessageEventMin
Blueprint = BotBlueprint

__all__ = (
    "ABCBotLabeler",
    "Bot",
    "Blueprint",
    "BotLabeler",
    "Message",
    "MessageEvent",
    "run_multibot",
    "rules",
    "views",
)
