import asyncio
from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import List
from typing import Optional
from typing import Union

from vkbottle.modules import logger

Task = Coroutine[Any, Any, Any]


class LoopWrapper:
    def __init__(
        self,
        *,
        on_startup: Optional[List[Task]] = None,
        on_shutdown: Optional[List[Task]] = None,
        tasks: Optional[List[Task]] = None,
    ):
        self.on_startup = on_startup or []
        self.on_shutdown = on_shutdown or []
        self.tasks = tasks or []

    def run_forever(self, loop: Optional[AbstractEventLoop] = None):
        if not len(self.tasks):
            logger.warn("You ran loop with 0 tasks. Is it ok?")

        loop = loop or get_event_loop()

        try:
            [loop.run_until_complete(startup_task) for startup_task in self.on_startup]

            for task in self.tasks:
                loop.create_task(task)

            loop.run_forever()
        finally:
            [loop.run_until_complete(shutdown_task) for shutdown_task in self.on_shutdown]
            if loop.is_running():
                loop.close()

    def add_task(self, task: Union[Task, Callable[..., Task]]):
        if asyncio.iscoroutinefunction(task):  # type: ignore
            self.tasks.append(task())  # type: ignore
        elif asyncio.iscoroutine(task):  # type: ignore
            self.tasks.append(task)  # type: ignore
        else:
            raise TypeError("Task should be coroutine or coroutine function")
