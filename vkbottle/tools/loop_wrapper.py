import asyncio
import contextlib
import warnings
from asyncio import get_event_loop
from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any, Callable, List, NoReturn, Optional, Union

from typing_extensions import deprecated

from vkbottle.modules import logger

from .delayed_task import DelayedTask

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    Task = Coroutine[Any, Any, Any]


class LoopWrapper:
    """Loop Wrapper for vkbottle manages startup, shutdown and main tasks,
    creates loop and runs it forever"""

    def __init__(
        self,
        *,
        on_startup: Optional[List["Task"]] = None,
        on_shutdown: Optional[List["Task"]] = None,
        tasks: Optional[List["Task"]] = None,
        loop: Optional["AbstractEventLoop"] = None,
    ) -> None:
        self.on_startup = on_startup or []
        self.on_shutdown = on_shutdown or []
        self.tasks = tasks or []
        self.loop = loop
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    @deprecated(
        "auto_reload is deprecated, instead, install watchfiles",
        category=FutureWarning,
        stacklevel=0,
    )
    def auto_reload(self) -> bool:
        return False

    @auto_reload.setter
    def auto_reload(self, value: bool) -> None:
        warnings.warn(
            "auto_reload is deprecated, instead, install watchfiles",
            FutureWarning,
            stacklevel=0,
        )

    @deprecated(
        "Deprecated. Use run() instead",
        category=FutureWarning,
        stacklevel=0,
    )
    def run_forever(self):
        logger.warning("run_forever() is deprecated. Use run() instead")
        self.run()

    def run(self) -> NoReturn:  # type: ignore
        """Runs startup tasks and makes the loop running until all tasks are done"""

        if not self.tasks:
            logger.warning("You ran loop with 0 tasks. Is it ok?")

        self._running = True
        self.loop = get_event_loop() if self.loop is None else self.loop

        for startup_task in self.on_startup:
            self.loop.run_until_complete(startup_task)

        while self.tasks:
            self.loop.create_task(self.tasks.pop(0))

        tasks = asyncio.all_tasks(self.loop)
        try:
            while tasks:
                tasks_results, _ = self.loop.run_until_complete(
                    asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
                )
                for task_result in tasks_results:
                    try:
                        task_result.result()
                    except Exception as exc:  # noqa: PERF203
                        logger.exception(exc)
                tasks = asyncio.all_tasks(self.loop)
        except KeyboardInterrupt:
            print(flush=True)  # Blank print for ^C # noqa: T201
            logger.info("Caught keyboard interrupt. Shutting down...")
            task_to_cancel = asyncio.gather(*tasks)
            task_to_cancel.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                self.loop.run_until_complete(task_to_cancel)
        finally:
            for shutdown_task in self.on_shutdown:
                self.loop.run_until_complete(shutdown_task)
            if self.loop.is_running():
                self.loop.close()

    def add_task(self, task: Union["Task", Callable[..., "Task"]]):
        """Adds tasks to be ran in run_forever or run it immediately if loop is already running
        :param task: coroutine / coroutine function with zero arguments
        """
        if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):
            task = task()  # type: ignore
        elif not asyncio.iscoroutine(task):
            msg = "Task should be coroutine or coroutine function"
            raise TypeError(msg)

        if self.loop and self.loop.is_running():
            self.loop.create_task(task)
        else:
            self.tasks.append(task)

    def interval(
        self,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
    ) -> Callable[[Callable], Callable]:
        """A tiny template to wrap repeated tasks with decorator
        >>> lw = LoopWrapper()
        >>> @lw.interval(seconds=5)
        >>> async def repeated_function():
        >>>     print("This will be logged every five seconds")
        >>> lw.run()
        """

        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: Callable):
            self.add_task(DelayedTask(seconds, func))
            return func

        return decorator

    def timer(
        self,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
    ) -> Callable[[Callable], Callable]:
        """A tiny template to wrap tasks with timer
        >>> lw = LoopWrapper()
        >>> @lw.timer(seconds=5)
        >>> async def delayed_function():
        >>>     print("This will after 5 seconds")
        >>> lw.run()
        """
        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        def decorator(func: Callable):
            self.add_task(DelayedTask(seconds, func, do_break=True))
            return func

        return decorator


__all__ = ("LoopWrapper",)
