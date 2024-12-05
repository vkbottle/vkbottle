from vkbottle.framework.labeler import UserLabeler

from .dispatch.rules import base as rules
from .dispatch.views import user as views
from .framework.user import User, UserBlueprint, run_multibot
from .tools.mini_types.user import MessageMin

Message = MessageMin
Blueprint = UserBlueprint


__all__ = (
    "Blueprint",
    "Message",
    "User",
    "UserLabeler",
    "rules",
    "run_multibot",
    "views",
)
