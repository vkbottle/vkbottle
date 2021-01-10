from . import bot
from . import user
from .bot import bot_message_min
from .user import user_message_min


class BotTypes:
    Message = bot.MessageMin


class UserTypes:
    Message = user.MessageMin