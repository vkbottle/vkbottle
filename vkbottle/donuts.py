from .framework import Bot
from .types import Message
import typing
import asyncio


async def with_timeout(timeout: int, coro):
    await asyncio.sleep(timeout)
    await coro


class DonutError(Exception):
    pass


class Donuts:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
    @staticmethod
    def typing_state(close=False):
        """
        Set typing state during the function is performing
        :param close:
        :return:
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                args: typing.List[Message] = [
                    ans for ans in args if type(ans) is Message
                ]
                if not len(args):
                    raise DonutError("Function should contain Message argument")

                await args[0].api[0].request(
                    "messages",
                    "setActivity",
                    {"user_id": args[0].peer_id, "type": "typing"},
                )

                return await func(*args, **kwargs)
            return wrapper
        return decorator

    def with_timeout(self, timeout: int):
        """
        Set timeout before handler performing
        :param timeout: timeout in seconds
        :return:
        """

        def decorator(func):
            async def wrapper(*args, **kwargs):
                self.bot.loop.create_task(
                    with_timeout(timeout, func(*args, **kwargs))
                )
                return
            return wrapper
        return decorator


