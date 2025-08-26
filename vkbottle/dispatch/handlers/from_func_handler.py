from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from vkbottle.tools.magic import magic_bundle

from .abc import ABCHandler, Event

if TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule


class FromFuncHandler(ABCHandler[Event]):
    def __init__(self, handler: Callable, *rules: "ABCRule", blocking: bool = True):
        self.handler = handler
        self.rules = rules
        self.blocking = blocking

    async def filter(
        self, event: Event, context: Optional[dict[str, Any]] = None
    ) -> Union[dict, bool]:
        rule_context = (context or {}).copy()
        for rule in self.rules:
            result = await rule.check(
                event,
                **magic_bundle(rule.check, rule_context),
            )
            if result is False or result is None:
                return False
            elif result is True:
                continue
            rule_context.update(result)
        return rule_context

    async def handle(self, event: Event, **context: Any) -> Any:
        return await self.handler(event, **magic_bundle(self.handler, context))

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

    def __repr__(self) -> str:
        return f"<FromFuncHandler {self.handler.__name__} blocking={self.blocking} rules={self.rules}>"


__all__ = ("FromFuncHandler",)
