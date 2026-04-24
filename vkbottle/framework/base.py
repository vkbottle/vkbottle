import asyncio
from abc import ABC
from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any, NoReturn

from typing_extensions import deprecated

from vkbottle.framework.abc import ABCFramework
from vkbottle.modules import logger
from vkbottle.tools._runner import run as _run

if TYPE_CHECKING:
    from vkbottle.dispatch import ABCRouter
    from vkbottle.polling import ABCPolling
    from vkbottle.tools.loop_wrapper import LoopWrapper

_Task = Coroutine[Any, Any, Any]


class BaseFramework(ABCFramework, ABC):
    router: "ABCRouter"
    on_startup: list[_Task]
    on_shutdown: list[_Task]
    startup_tasks: list[_Task]
    _loop_wrapper: "LoopWrapper | None"

    async def run_polling(self, custom_polling: "ABCPolling | None" = None) -> NoReturn:  # type: ignore[misc,return-value]
        _polling = custom_polling or self.polling
        logger.info("Starting {} for {!r}", type(_polling).__name__, _polling.api)

        pending: set[asyncio.Task] = set()

        async for event in _polling.listen():
            logger.debug("New event was received: {!r}", event)

            for update in event.get("updates", []):
                task = asyncio.create_task(self.router.route(update, _polling.api))
                pending.add(task)
                task.add_done_callback(pending.discard)

    def run(self) -> NoReturn:  # type: ignore[return-value]
        logger.info("Loop will be run forever")

        startup = list(self.on_startup)
        shutdown = list(self.on_shutdown)

        tasks: list[_Task] = list(self.startup_tasks)
        tasks.append(self.run_polling())

        if self._loop_wrapper is not None:
            startup = list(self._loop_wrapper.on_startup) + startup
            shutdown = shutdown + list(self._loop_wrapper.on_shutdown)

            tasks = list(self._loop_wrapper.tasks) + tasks

            self._loop_wrapper.on_startup = []
            self._loop_wrapper.on_shutdown = []

            self._loop_wrapper.tasks = []

        self.on_startup = []
        self.on_shutdown = []
        self.startup_tasks = []

        _run(*tasks, on_startup=startup, on_shutdown=shutdown)

    @deprecated(
        "Deprecated. Use run() instead",
        category=FutureWarning,
        stacklevel=0,
    )
    def run_forever(self) -> NoReturn:
        self.run()


__all__ = ("BaseFramework",)
