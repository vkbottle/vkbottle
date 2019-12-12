from .framework import Bot
from .types import Message
import typing
import asyncio


class DonutError(Exception):
    pass


class Donuts:
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
