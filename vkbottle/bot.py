from vkbottle.framework.labeler import BotLabeler

from .dispatch.rules import base as rules
from .dispatch.views import bot as views
from .framework.bot import Bot, BotBlueprint, run_multibot
from .tools.dev.mini_types.bot import MessageEventMin, MessageMin

Message = MessageMin
MessageEvent = MessageEventMin
Blueprint = BotBlueprint

__all__ = (
    "Bot",
    "Blueprint",
    "BotLabeler",
    "Message",
    "MessageEvent",
    "run_multibot",
    "rules",
    "views",
)
