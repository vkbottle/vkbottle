from vkbottle.framework.labeler import BotLabeler

from .dispatch.rules import base as rules
from .dispatch.views import bot as views
from .framework.bot import Bot, BotBlueprint, run_multibot
from .tools.dev.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = BotBlueprint

__all__ = (
    "Bot",
    "Blueprint",
    "BotLabeler",
    "Message",
    "run_multibot",
    "rules",
    "views",
)
