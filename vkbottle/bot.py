from typing_extensions import deprecated  # type: ignore

from vkbottle.framework.labeler import BotLabeler

from .dispatch.rules import base as rules
from .dispatch.views import bot as views
from .framework.bot import Bot, BotBlueprint, run_multibot
from .tools.mini_types.bot import MessageEventMin, MessageMin

Message = MessageMin
MessageEvent = MessageEventMin


@deprecated(
    "Blueprints was deprecated and will be removed in future releases, "
    "read about new code separation method in documentation: \n"
    "https://vkbottle.rtfd.io/ru/latest/tutorial/code-separation/",
    stacklevel=0,
)
class Blueprint(BotBlueprint): ...


__all__ = (
    "Blueprint",
    "Bot",
    "BotLabeler",
    "Message",
    "MessageEvent",
    "rules",
    "run_multibot",
    "views",
)
