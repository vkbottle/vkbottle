from .dispatch.rules import bot as rules
from .dispatch.views import bot as views
from .framework.bot import ABCBotLabeler, Bot, BotBlueprint, BotLabeler, run_multibot
from .tools.dev.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = BotBlueprint
