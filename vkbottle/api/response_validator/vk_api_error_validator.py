import contextvars
from typing import TYPE_CHECKING, Any

from vkbottle.exception_factory import CaptchaError, VKAPIError
from vkbottle.modules import logger

from .abc import ABCResponseValidator

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


MAX_CAPTCHA_ATTEMPTS = 5
# Per-request captcha retry counter (isolated per task/async-context) so a VK that
# keeps returning captcha cannot drive unbounded recursion.
_captcha_attempts: contextvars.ContextVar[int] = contextvars.ContextVar(
    "vkbottle_captcha_attempts", default=0
)


class VKAPIErrorResponseValidator(ABCResponseValidator):
    """Default vk api error response validator
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api/response-validator
    """

    async def validate(
        self,
        method: str,
        data: dict[str, Any],
        response: Any,
        ctx_api: "ABCAPI | API",
    ) -> Any:
        if not isinstance(response, dict):
            request_params = [{"key": key, "value": value} for key, value in data.items()]
            raise VKAPIError[1](
                error_msg=f"Unknown response from {method}: {response}",
                request_params=request_params,
            )

        if "error" not in response:
            if "response" not in response:
                request_params = [{"key": key, "value": value} for key, value in data.items()]
                raise VKAPIError[1](
                    error_msg=f"Unknown response from {method}: {response}",
                    request_params=request_params,
                )

            if isinstance(response["response"], list) and any(
                "error" in item for item in response["response"] if isinstance(item, dict)
            ):
                logger.info("API error(s) in response wasn't handled: {!r}", response["response"])

            return response

        if ctx_api.ignore_errors:
            return None
        error = response["error"]
        code = error.pop("error_code")

        if VKAPIError[code] is CaptchaError and ctx_api.captcha_handler is not None:
            attempts = _captcha_attempts.get()
            if attempts >= MAX_CAPTCHA_ATTEMPTS:
                raise VKAPIError[code](**error)
            token = _captcha_attempts.set(attempts + 1)
            try:
                key = await ctx_api.captcha_handler(CaptchaError(**error))  # type: ignore
                return await ctx_api.request(
                    method,
                    data={**data, "captcha_sid": error["captcha_sid"], "captcha_key": key},
                )
            finally:
                _captcha_attempts.reset(token)

        raise VKAPIError[code](**error)


__all__ = ("VKAPIErrorResponseValidator",)
