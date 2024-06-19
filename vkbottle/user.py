from typing_extensions import deprecated  # type: ignore

from vkbottle.framework.labeler import UserLabeler

from .dispatch.rules import base as rules
from .dispatch.views import user as views
from .framework.user import User, UserBlueprint, run_multibot
from .tools.mini_types.bot import MessageMin

Message = MessageMin


@deprecated(
    "Blueprints was deprecated and will be removed in future releases, "
    "read about new code separation method in documentation: \n"
    "https://vkbottle.rtfd.io/ru/latest/tutorial/code-separation/",
    stacklevel=0,
)
class Blueprint(UserBlueprint): ...


__all__ = (
    "Blueprint",
    "Message",
    "User",
    "UserLabeler",
    "rules",
    "run_multibot",
    "views",
)
