from .abc import ABCRouter
from .views import bot
from vkbottle.dispatch.middlewares import BaseMiddleware
from typing import List


class BotRouter(ABCRouter):
    views = {"message": bot.MessageView()}
    middlewares: List["BaseMiddleware"] = []

    async def route(self, event: dict):
        for view in self.views.values():
            if not await view.process_event(event):
                continue
            return await view.handle_event(event)
