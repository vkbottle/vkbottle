from collections.abc import Callable, Coroutine
from typing import Any

from .delayed_task import DelayedTask

_Handler = Callable[..., Coroutine[Any, Any, Any]]


def _total_seconds(seconds: int, minutes: int, hours: int, days: int) -> int:
    return seconds + minutes * 60 + hours * 3600 + days * 86400


def interval(
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    days: int = 0,
) -> Callable[[_Handler], DelayedTask]:
    """Wrap a coroutine function into a task that repeats forever at a fixed delay.

    Usage::

        @interval(seconds=5)
        async def tick():
            ...

        # Inside an async context:
        asyncio.create_task(tick())

        # Or register on the framework:
        bot.startup_tasks.append(tick())
    """

    total = _total_seconds(seconds, minutes, hours, days)

    def decorator(func: _Handler) -> DelayedTask:
        return DelayedTask(total, func)

    return decorator


def timer(
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    days: int = 0,
) -> Callable[[_Handler], DelayedTask]:
    """Wrap a coroutine function into a one-shot task that runs after a delay.

    Usage::

        @timer(seconds=5)
        async def later():
            ...

        asyncio.create_task(later())
    """

    total = _total_seconds(seconds, minutes, hours, days)

    def decorator(func: _Handler) -> DelayedTask:
        return DelayedTask(total, func, do_break=True)

    return decorator


__all__ = ("interval", "timer")
