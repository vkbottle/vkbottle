from asyncio import sleep
from typing import Any, Callable, Coroutine


class DelayedTask:
    def __init__(
        self,
        seconds: int,
        handler: Callable[..., Coroutine[Any, Any, Any]],
        do_break: bool = False,
    ):
        self.seconds = seconds
        self.handler = handler
        self.do_break = do_break

    async def __call__(self, *args, **kwargs):
        while True:
            await sleep(self.seconds)
            await self.handler(*args, **kwargs)
            if self.do_break:
                break
