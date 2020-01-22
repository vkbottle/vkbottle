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

    def in_loop(self, loop: int):
        """
        Make loops..
        :param loop:
        :return:
        """

        def decorator(func):
            async def wrapper(*args, **kwargs):
                print(args, kwargs)
                for iteration in range(0, loop):
                    self.bot.loop.create_task(func(*args, **kwargs))
                return

            return wrapper

        return decorator

    def typing_state(self):
        """
        Set typing state during the function is performing
        :param close:
        :return:
        """

        def decorator(func):
            async def wrapper(*args, **kwargs):

                await self.bot.api.request(
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
                self.bot.loop.create_task(with_timeout(timeout, func(*args, **kwargs)))
                return

            return wrapper

        return decorator

    def mark_as_read(self):
        """
        Mark message as read
        :return:
        """

        def decorator(func):
            async def wrapper(*args, **kwargs):

                await self.bot.api.request(
                    "messages",
                    "markAsRead",
                    {
                        "start_message_id": args[0].id,
                        "message_ids": args[0].id,
                        "peer_id": args[0].peer_id,
                    },
                )

                return await func(*args, **kwargs)

            return wrapper

        return decorator
