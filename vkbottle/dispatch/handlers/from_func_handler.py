from typing import TYPE_CHECKING, Any, Callable, Union, Optional

from .abc import ABCHandler
from vkbottle.tools.dev.utils import call_by_signature

if TYPE_CHECKING:
    from vkbottle_types.events import Event

    from vkbottle.dispatch.rules import ABCRule


class FromFuncHandler(ABCHandler):
    def __init__(self, handler: Callable, *rules: "ABCRule", blocking: bool = True):
        self.handler = handler
        self.rules = rules
        self.blocking = blocking

    async def filter(
        self,
        event: "Event",
        context_variables: Optional[dict] = None
    ) -> Union[dict, bool]:
        rule_context = {}  # for compatability only
        for rule in self.rules:
            result = await call_by_signature(
                rule.check,
                event,
                context_variables=context_variables
            )
            if result is False or result is None:
                return False
            elif result is True:
                continue
            rule_context.update(result)
        return rule_context

    async def handle(self, event: "Event", **context) -> Any:
        return await call_by_signature(self.handler, event, **context)

    def __eq__(self, obj: object) -> bool:
        """
        Sugar to easily check if the function is actual handler.

        >>> my_handler = lambda *args, **kwargs: None
        >>> middleware_handlers = [FromFuncHandler(my_handler)]
        >>> my_handler in middleware_handlers
        True
        """
        if callable(obj):
            return self.handler == obj
        return super().__eq__(obj)

    def __repr__(self):
        return f"<FromFuncHandler {self.handler.__name__} blocking={self.blocking} rules={self.rules}>"
