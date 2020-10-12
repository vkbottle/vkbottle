from .abc import ABCRouter
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.dispatch.views import ABCView
from vkbottle.api.abc import ABCAPI
from vkbottle.modules import logger
from vkbottle.exception_factory.error_handler import ErrorHandler
from typing import Dict, NoReturn


class BotRouter(ABCRouter):
    error_handler = ErrorHandler(redirect_arguments=True)

    @error_handler.wraps_error_handler()
    async def route(self, event: dict, ctx_api: "ABCAPI") -> NoReturn:  # type: ignore
        logger.debug("Routing update {}".format(event))
        for view in self.views.values():
            if not await view.process_event(event):
                continue
            await view.handle_event(event, ctx_api)

    def construct(self, views: Dict[str, "ABCView"]) -> "BotRouter":
        self.views = views
        return self
