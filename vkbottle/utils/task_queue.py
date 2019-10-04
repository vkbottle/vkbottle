import asyncio
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)


class TaskQueue:
    """
    Task manager represent to user high-level API of asyncio interface (Less part :))
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.tasks: List[Callable] = []
        self.loop: asyncio.AbstractEventLoop = loop

    def run(self,
            shutdown: Callable = None,
            startup: Callable = None,
            asyncio_debug_mode: bool = False,
            ):
        """
        Method which run event loop
        :param shutdown: coroutine which runned after complete tasks
        :param startup: coroutine which runned before start main tasks
        :param asyncio_debug_mode: asyncio debug mode state
        :return:
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
        if asyncio.iscoroutinefunction(task):
            self.tasks.append(task)
            logger.debug(f"Task {task.__name__} added!")
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")

    def run_task(self, task: Callable):
        """
        Create task in loop
        :param task:
        :return:
        """

        self.loop.create_task(task())
