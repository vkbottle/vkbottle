from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Generic, List, TypeVar

if TYPE_CHECKING:
    from vkbottle.api.abc import ABCAPI
    from vkbottle.dispatch.dispenser.abc import ABCStateDispenser

from vkbottle.modules import logger

from .view import ABCView

T_contra = TypeVar("T_contra", list, dict, contravariant=True)


class ABCRawEventView(ABCView[T_contra], Generic[T_contra]):
    handlers: Dict[Any, List]

    @abstractmethod
    def get_handler_basements(self, event: T_contra) -> List:
        pass

    @abstractmethod
    def get_event_model(self, handler_basement, event: T_contra):
        pass

    @staticmethod
    @abstractmethod
    def get_event_type(event: T_contra):
        pass

    async def handle_event(
        self, event: T_contra, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:
        logger.debug("Handling event ({}) with message view".format(self.get_event_type(event)))

        context_variables: dict = {}
        handle_responses = []
        handlers = []

        mw_instances = await self.pre_middleware(event, context_variables)
        if mw_instances is None:
            logger.info("Handling stopped, pre_middleware returned error")
            return

        for handler_basement in self.get_handler_basements(event):
            event_model = self.get_event_model(handler_basement, event)

            if isinstance(event_model, dict):
                event_model["ctx_api"] = ctx_api
            else:
                setattr(event_model, "unprepared_ctx_api", ctx_api)

            result = await handler_basement.handler.filter(event_model)
            logger.debug("Handler {} returned {}".format(handler_basement.handler, result))

            if result is False:
                continue

            elif isinstance(result, dict):
                context_variables.update(result)

            handler_response = await handler_basement.handler.handle(
                event_model, **context_variables
            )
            handle_responses.append(handler_response)
            handlers.append(handler_basement.handler)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager,
                    handler_response,
                    event_model,
                    context_variables,
                )

            if handler_basement.handler.blocking:
                break

        await self.post_middleware(mw_instances, handle_responses, handlers)
