from typing import Dict

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser import ABCStateDispenser
from vkbottle.dispatch.views import ABCView
from vkbottle.exception_factory import ABCErrorHandler
from vkbottle.modules import logger

from .abc import ABCRouter


class BotRouter(ABCRouter):
    async def route(self, event: dict, ctx_api: "ABCAPI") -> None:
        logger.debug("Routing update {}".format(event))

        for view in self.views.values():
            try:
                if not await view.process_event(event):
                    continue
                await view.handle_event(event, ctx_api, self.state_dispenser)
            except BaseException as e:
                await self.error_handler.handle(e)

    def construct(
        self,
        views: Dict[str, "ABCView"],
        state_dispenser: ABCStateDispenser,
        error_handler: ABCErrorHandler,
    ) -> "BotRouter":
        self.views = views
        self.state_dispenser = state_dispenser
        self.error_handler = error_handler
        return self
