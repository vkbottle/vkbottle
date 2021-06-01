from abc import abstractmethod
from typing import Any, Union

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle.modules import logger

from .view import ABCView


class ABCRawEventView(ABCView):
    @abstractmethod
    def get_handler_basement(self, event):
        ...

    @abstractmethod
    def get_event_model(self, handler_basement, event):
        ...

    @staticmethod
    @abstractmethod
    def get_logger_event_value(event):
        ...

    async def handle_event(
        self, event: Union[list, dict], ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:
        logger.debug(
            "Handling event ({}) with message view".format(self.get_logger_event_value(event))
        )

        handler_basement = self.get_handler_basement(event)
        context_variables: dict = {}

        event_model = self.get_event_model(handler_basement, event)

        if isinstance(event_model, dict):
            event_model["ctx_api"] = ctx_api
        else:
            setattr(event_model, "unprepared_ctx_api", ctx_api)

        error = await self.pre_middleware(event_model, context_variables)
        if error:
            return logger.info("Handling stopped, pre_middleware returned error")

        result = await handler_basement.handler.filter(event_model)
        logger.debug("Handler {} returned {}".format(handler_basement.handler, result))

        if result is False:
            return

        elif isinstance(result, dict):
            context_variables.update(result)

        handler_response = await handler_basement.handler.handle(event_model, **context_variables)

        return_handler = self.handler_return_manager.get_handler(handler_response)
        if return_handler is not None:
            await return_handler(
                self.handler_return_manager,
                handler_response,
                event_model,
                context_variables,
            )

        await self.post_middleware([handler_response], [handler_basement.handler])
