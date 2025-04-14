from abc import ABC
from typing import TYPE_CHECKING, NoReturn, Optional

from vkbottle.framework.abc import ABCFramework
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle.dispatch import ABCRouter
    from vkbottle.polling import ABCPolling
    from vkbottle.tools.loop_wrapper import LoopWrapper


class BaseFramework(ABCFramework, ABC):
    router: "ABCRouter"
    loop_wrapper: "LoopWrapper"

    async def run_polling(self, custom_polling: Optional["ABCPolling"] = None) -> NoReturn:
        async def polling() -> NoReturn:  # type: ignore
            _polling = custom_polling or self.polling
            logger.info("Starting {} for {!r}", type(_polling).__name__, _polling.api)

            async for event in _polling.listen():
                logger.debug("New event was received: {!r}", event)
                for update in event.get("updates", []):
                    self.loop_wrapper.add_task(self.router.route(update, _polling.api))

        if not self.loop_wrapper.is_running:
            self.loop_wrapper.add_task(polling())
            self.loop_wrapper.run()
        else:
            await polling()

    def run_forever(self) -> NoReturn:
        logger.info("Loop will be run forever")
        self.loop_wrapper.add_task(self.run_polling())
        self.loop_wrapper.run()


__all__ = ("BaseFramework",)
