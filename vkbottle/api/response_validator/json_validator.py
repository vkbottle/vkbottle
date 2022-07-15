import contextlib
from typing import TYPE_CHECKING, Any, NoReturn, Optional, Union

from vkbottle.modules import json, logger

from .abc import ABCResponseValidator

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class JSONResponseValidator(ABCResponseValidator):
    """Default response json-parse validator
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/response-validator.md
    """

    def __init__(self, context: Optional[dict] = None):
        self.context = context or {}

    async def validate(
        self,
        method: str,
        data: dict,
        response: Any,
        ctx_api: Union["ABCAPI", "API"],
    ) -> Union[Any, NoReturn]:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            with contextlib.suppress(ValueError):
                return json.loads(response)

        if self.context.get("reschedule"):
            return None

        logger.info(
            "VK returned object of invalid type ({}). Request will be rescheduled with {}",
            type(response).__name__,
            ctx_api.request_rescheduler.__class__.__name__,
        )
        self.context["reschedule"] = True
        response = await self.validate(
            method,
            data,
            await ctx_api.request_rescheduler.reschedule(ctx_api, method, data, response),
            ctx_api,
        )
        self.context.pop("reschedule")
        return response
