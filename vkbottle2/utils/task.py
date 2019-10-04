import asyncio
from asyncio import iscoroutinefunction
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)


class TaskQueue:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.tasks: List[Callable] = []
        self.loop: asyncio.AbstractEventLoop = loop

    def run(self,
            shutdown: Callable = None,
            startup: Callable = None,
            asyncio_debug_mode: bool = False,
            ):
        """
        Run events
        """
        if len(self.tasks) < 1:
            raise RuntimeError("Count of tasks - 0. Add tasks.")
        try:
            if startup is not None:
                self.loop.run_until_complete(startup())

            if asyncio_debug_mode:
                self.loop.set_debug(True)

            [self.loop.create_task(task()) for task in self.tasks]

            logger.info("Loop started!")
            self.loop.run_forever()

        finally:
            if shutdown is not None:
                self.loop.run_until_complete(shutdown())

    def close(self):
        """
        Close event loop manually
        :return:
        """
        self.loop.close()

    def add_task(self, task: Callable):
        """
        Add task to loop when loop don`t started.
        :param task: coroutine for run in loop
        :return:
        """
        if iscoroutinefunction(task):
            self.tasks.append(task)
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")

    def run_task(self, task: Callable):
        """
        Create task in loop
        :param task:
        :return:
        """

        self.loop.create_task(task())
