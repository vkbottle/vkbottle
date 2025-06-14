from . import bot, user


class BotTypes:
    Message = bot.MessageMin
    MessageEvent = bot.MessageEventMin


class UserTypes:
    Message = user.MessageMin


__all__ = ("BotTypes", "UserTypes")
