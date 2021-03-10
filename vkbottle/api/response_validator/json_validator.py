import typing

from vkbottle.modules import json, logger

from .abc import ABCResponseValidator

if typing.TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class JSONResponseValidator(ABCResponseValidator):
    """ Default response json-parse validator
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/response-validator.md
    """

    async def validate(
        self,
        method: str,
        data: dict,
        response: typing.Any,
        ctx_api: typing.Union["ABCAPI", "API"],
    ) -> typing.Any:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            return json.loads(response)

        logger.info(
            f"VK returned object of invalid type ({type(response)})."
            f"Request will be rescheduled with {ctx_api.request_rescheduler.__class__.__name__!r}"
        )

        return await self.validate(
            method,
            data,
            await ctx_api.request_rescheduler.reschedule(ctx_api, method, data, response),
            ctx_api,
        )
