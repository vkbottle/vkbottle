from typing import Callable
from asyncio import iscoroutinefunction

from ..api import Api
from ..framework import Bot
from .exceptions import FetchMethodError


async def assign_function(*args, **kwargs):
    raise FetchMethodError("Please assign FM Function")


def assigned(iterator):
    return len(iterator) > 0


class FetchMethod:
    def __init__(self, bot: Bot):
        self.api: Api = bot.api

    def __call__(self, desc: str = None):
        return Fetching(self.api)


class Fetching:
    def __init__(self, api):
        self.api: Bot.api = api
        self.running_func: Callable = assign_function
        self.args: list = []
        self.kwargs: dict = {}

    def __call__(self, function: Callable = None, *args, IGNORE_CORO=True, **kwargs):
        if not iscoroutinefunction(function) and not IGNORE_CORO:
            raise FetchMethodError("Function is not awaitable (make it async)")
        self.running_func = function or self.running_func
        if assigned(args):
            self.args = args
        if assigned(kwargs):
            self.kwargs = kwargs

        return self

    async def run(self):
        response = await self.running_func(*self.args, **self.kwargs)
        return response

    async def run_without_response(self):
        await self.running_func(*self.args, **self.kwargs)
        return self
