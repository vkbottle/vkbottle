from vkbottle.framework.labeler import UserLabeler

from .dispatch.rules import base as rules
from .dispatch.views import user as views
from .framework.user import User, UserBlueprint, run_multibot
from .tools.dev.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = UserBlueprint

__all__ = (
    "User",
    "Blueprint",
    "UserLabeler",
    "Message",
    "run_multibot",
    "rules",
    "views",
)
