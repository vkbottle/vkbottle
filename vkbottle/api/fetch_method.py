from ..framework import Bot
from .exceptions import FetchMethodError
from asyncio import iscoroutinefunction
from typing import Callable, Optional


async def assign_function(*args, **kwargs):
    raise FetchMethodError('Please assign FM Function')


def assigned(iterator):
    if len(iterator) > 0:
        return True


class FetchMethod(object):
    def __init__(self, bot: Bot):
        self.api: Bot.api = bot.api

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
            raise FetchMethodError('Function is not awaitable (make it async)')
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
