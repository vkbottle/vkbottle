from .abc import ABCHandler
from vkbottle.dispatch.rules import ABCRule
from typing import Tuple, Any, Callable


class FromFuncHandler(ABCHandler):
    def __init__(self, handler: Callable, *rules: "ABCRule", blocking: bool = True):
        self.handler = handler
        self.rules = rules
        self.blocking = blocking

    async def filter(self, event: Any) -> bool:
        for rule in self.rules:
            if not await rule.check(event):
                return False
        return True

    async def handle(self, event: Any) -> Any:
        return await self.handler(event)
