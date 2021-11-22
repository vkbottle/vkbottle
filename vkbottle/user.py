from .dispatch.rules import base as rules
from .dispatch.views import user as views
from .framework.user import ABCUserLabeler, User, UserBlueprint, UserLabeler, run_multibot
from .tools.dev.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = UserBlueprint

__all__ = (
    "User",
    "UserBlueprint",
    "UserLabeler",
    "ABCUserLabeler",
    "run_multibot",
    "rules",
    "views",
)
