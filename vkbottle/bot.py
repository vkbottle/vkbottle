from .dispatch.rules import bot
from .framework.bot import ABCBotLabeler, Bot, BotBlueprint, BotLabeler, run_multibot
from .tools.dev_tools.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = BotBlueprint
rules = bot
