import asyncio
import typing
import warnings

from ..utils.logger import logger
from .auto_reload import _auto_reload

CallableAwaitable = typing.Union[typing.Callable, typing.Awaitable]


class TaskManager:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        *,
        on_shutdown: typing.Callable = None,
        on_startup: typing.Callable = None,
        auto_reload: bool = False,
        auto_reload_dir: str = ".",
        asyncio_debug_mode: bool = False,
    ):
        self.tasks: typing.List[typing.Callable] = []

        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()

        self.on_shutdown: CallableAwaitable = on_shutdown
        self.on_startup: CallableAwaitable = on_startup
        self.auto_reload: bool = auto_reload
        self.auto_reload_dir: str = auto_reload_dir

        self.loop.set_debug(asyncio_debug_mode)

    def run(
        self, **abandoned,
    ):
        if len(abandoned):
            warnings.warn("Pass options through __init__")
            for option in abandoned:
                setattr(self, option, abandoned[option])

        if len(self.tasks) < 1:
            raise RuntimeError("Count of tasks - 0. Add tasks.")
        try:
            if self.on_startup is not None:
                self.loop.run_until_complete(self.on_startup())

            if self.auto_reload:
                self.loop.create_task(_auto_reload(self.auto_reload_dir))

            [self.loop.create_task(task) for task in self.tasks]

            self.loop.run_forever()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
            self.close()

        finally:
            if self.on_shutdown is not None:
                self.loop.run_until_complete(self.on_shutdown())
            if not self.loop.is_running():
                self.close()

    def close(self):
        self.loop.close()

    def add_task(self, task: typing.Union[typing.Coroutine, typing.Callable]):
        if asyncio.iscoroutinefunction(task):
            self.tasks.append(task())
        elif asyncio.iscoroutine(task):
            self.tasks.append(task)
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")

    def run_task(self, task: typing.Union[typing.Coroutine, typing.Callable]):
        if asyncio.iscoroutinefunction(task):
            self.loop.create_task(task())
        elif asyncio.iscoroutine(task):
            self.loop.create_task(task)
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")
