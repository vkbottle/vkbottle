import asyncio
import contextlib
from collections.abc import Coroutine, Iterable
from typing import Any

from vkbottle.modules import logger

_Task = Coroutine[Any, Any, Any]


async def _drain(initial_tasks: Iterable[_Task]) -> None:
    spawned: set[asyncio.Task] = set()

    for task in initial_tasks:
        scheduled = asyncio.create_task(task)
        spawned.add(scheduled)
        scheduled.add_done_callback(spawned.discard)

    current = asyncio.current_task()

    while True:
        pending = {t for t in asyncio.all_tasks() if t is not current}

        if not pending:
            return

        done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_EXCEPTION)

        for done_task in done:
            if done_task.cancelled():
                continue

            exc = done_task.exception()

            if exc is not None:
                logger.opt(exception=exc).error("Unhandled exception in task")


def run(
    *tasks: _Task,
    on_startup: Iterable[_Task] = (),
    on_shutdown: Iterable[_Task] = (),
) -> None:
    """Run startup tasks, then main tasks, then shutdown tasks in a fresh event loop.

    Replacement for LoopWrapper.run() that does not depend on LoopWrapper itself.
    Exceptions inside tasks are logged but do not abort sibling tasks.
    Shutdown tasks run even if a KeyboardInterrupt is caught.
    """
    loop = asyncio.new_event_loop()

    try:
        asyncio.set_event_loop(loop)

        for task in on_startup:
            loop.run_until_complete(task)

        try:
            loop.run_until_complete(_drain(tasks))
        except KeyboardInterrupt:
            print(flush=True)  # noqa: T201

            logger.info("Caught keyboard interrupt. Shutting down...")
            pending = asyncio.all_tasks(loop)

            if pending:
                gathered = asyncio.gather(*pending, return_exceptions=True)
                gathered.cancel()

                with contextlib.suppress(asyncio.CancelledError):
                    loop.run_until_complete(gathered)
        finally:
            for task in on_shutdown:
                try:
                    loop.run_until_complete(task)
                except Exception:  # noqa: PERF203
                    logger.exception("Error in shutdown task")
    finally:
        if not loop.is_closed():
            loop.close()


__all__ = ("run",)
