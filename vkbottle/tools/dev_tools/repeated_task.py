from asyncio import sleep
from typing import Callable, Coroutine, Any

Handler = Callable[..., Coroutine[Any, Any, Any]]


class RepeatedTask:
    def __init__(self, seconds: int, handler: Handler):
        self.seconds = seconds
        self.handler = handler

    async def __call__(self, *args, **kwargs):
        while True:
            await sleep(self.seconds)
            await self.handler(*args, **kwargs)
