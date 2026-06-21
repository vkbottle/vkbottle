import contextlib
import contextvars
from typing import TYPE_CHECKING, Any

from vkbottle.modules import json, logger

from .abc import ABCResponseValidator

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

# Per-request (per-async-context) re-entrancy guard for the reschedule path.
# It must NOT live on the validator instance: the default validator is a single
# object shared by every API, so instance state would leak across concurrent
# in-flight requests. A ContextVar is isolated per task/context.
_rescheduling: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "vkbottle_json_validator_rescheduling", default=False
)


class JSONResponseValidator(ABCResponseValidator):
    """Default response json-parse validator
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api/response-validator
    """

    def __init__(self, context: dict[str, Any] | None = None):
        self.context = context or {}

    async def validate(
        self,
        method: str,
        data: dict[str, Any],
        response: Any,
        ctx_api: "ABCAPI | API",
    ) -> Any:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            with contextlib.suppress(ValueError):
                return json.loads(response)

        if _rescheduling.get():
            return None

        logger.info(
            "VK returned object of invalid type ({!r}). Request will be rescheduled with {!r}.",
            type(response).__name__,
            ctx_api.request_rescheduler.__class__.__name__,
        )
        token = _rescheduling.set(True)
        try:
            return await self.validate(
                method,
                data,
                await ctx_api.request_rescheduler.reschedule(ctx_api, method, data, response),
                ctx_api,
            )
        finally:
            _rescheduling.reset(token)


__all__ = ("JSONResponseValidator",)
