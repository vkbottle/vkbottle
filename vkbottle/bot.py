from .dispatch.rules import base as rules
from .dispatch.views import bot as views
from .framework.bot import ABCBotLabeler, Bot, BotBlueprint, BotLabeler, run_multibot
from .tools.dev.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = BotBlueprint

__all__ = (
    "ABCBotLabeler",
    "Bot",
    "Blueprint",
    "BotLabeler",
    "Message",
    "run_multibot",
    "rules",
    "views",
)
