import asyncio
import inspect
import warnings
from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, NoReturn

from typing_extensions import deprecated

from vkbottle.modules import logger

from ._runner import run as _run
from .delayed_task import DelayedTask
from .scheduling import interval as _interval
from .scheduling import timer as _timer

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    Task = Coroutine[Any, Any, Any]

_DEPRECATION_MESSAGE = (
    "LoopWrapper is deprecated. Use bot.run() / await bot.run_polling() directly, "
    "and register tasks via bot.on_startup, bot.on_shutdown, bot.startup_tasks. "
    "For scheduled coroutines use vkbottle.interval / vkbottle.timer."
)


class LoopWrapper:
    """Backward-compatibility facade over :func:`vkbottle.framework.runner.run`.

    Kept to avoid breaking existing user code; new code should not rely on this class.
    """

    def __init__(
        self,
        *,
        on_startup: list["Task"] | None = None,
        on_shutdown: list["Task"] | None = None,
        tasks: list["Task"] | None = None,
        loop: "AbstractEventLoop | None" = None,
    ) -> None:
        warnings.warn(_DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)

        self.on_startup: list[Task] = on_startup or []
        self.on_shutdown: list[Task] = on_shutdown or []

        self.tasks: list[Task] = tasks or []
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
    def run_forever(self) -> NoReturn:
        logger.warning("run_forever() is deprecated. Use run() instead")
        self.run()

    def run(self) -> NoReturn:  # type: ignore[misc]
        """Drain registered startup/main/shutdown tasks and block until completion."""
        self._running = True

        try:
            _run(
                *self.tasks,
                on_startup=self.on_startup,
                on_shutdown=self.on_shutdown,
            )
        finally:
            self._running = False
            self.tasks = []

            self.on_startup = []
            self.on_shutdown = []

    def add_task(self, task: "Task | Callable[..., Task]") -> None:
        """Schedule a coroutine to run in the loop.

        If called while the wrapper is already running the task is submitted to
        the current loop; otherwise it is buffered until :meth:`run` is called.
        """
        if inspect.iscoroutinefunction(task) or isinstance(task, DelayedTask):
            task = task()  # type: ignore[operator]
        elif not asyncio.iscoroutine(task):
            msg = "Task should be coroutine or coroutine function"
            raise TypeError(msg)

        try:
            running_loop = asyncio.get_running_loop()
        except RuntimeError:
            running_loop = None

        if running_loop is not None:
            running_loop.create_task(task)
        else:
            self.tasks.append(task)

    def interval(
        self,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Deprecated: use :func:`vkbottle.interval`."""
        decorator_impl = _interval(seconds=seconds, minutes=minutes, hours=hours, days=days)

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.add_task(decorator_impl(func))
            return func

        return decorator

    def timer(
        self,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Deprecated: use :func:`vkbottle.timer`."""
        decorator_impl = _timer(seconds=seconds, minutes=minutes, hours=hours, days=days)

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.add_task(decorator_impl(func))
            return func

        return decorator


__all__ = ("LoopWrapper",)
