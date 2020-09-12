from .abc import ABCRouter
from .views import bot
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.api.abc import ABCAPI
from vkbottle.modules import logger
from typing import List


class BotRouter(ABCRouter):
    views = {"message": bot.MessageView()}
    middlewares: List["BaseMiddleware"] = []

    async def route(self, event: dict, ctx_api: "ABCAPI"):
        logger.debug("Routing event {}".format(event))
        for view in self.views.values():
            if not await view.process_event(event):
                continue
            await view.handle_event(event, ctx_api)
