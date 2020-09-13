from .framework.bot import Bot, ABCBotLabeler, BotLabeler, run_multibot
from .tools.dev_tools.mini_types.bot import MessageMin
from .dispatch.rules import bot

Message = MessageMin
rules = bot
