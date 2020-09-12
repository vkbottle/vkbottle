from .abc import ABCHandler
from vkbottle.dispatch.rules import ABCRule
from typing import Union, Any, Callable


class FromFuncHandler(ABCHandler):
    def __init__(self, handler: Callable, *rules: "ABCRule", blocking: bool = True):
        self.handler = handler
        self.rules = rules
        self.blocking = blocking

    async def filter(self, event: Any) -> Union[dict, bool]:
        rule_context = {}
        for rule in self.rules:
            result = await rule.check(event)
            if result is False:
                return False
            elif result is True:
                continue
            rule_context.update(result)
        return rule_context

    async def handle(self, event: Any, **context) -> Any:
        return await self.handler(event, **context)

    def __repr__(self):
        return f"<FromFuncHandler {self.handler.__name__} blocking={self.blocking} rules={self.rules}>"
