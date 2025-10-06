from typing import Any

import pydantic

from vkbottle.modules import json

from .abc import ABCRequestValidator


class TranslateFriendlyTypesRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict[str, Any]) -> dict[str, Any]:
        for k, v in request.copy().items():
            if isinstance(v, list):
                request[k] = ",".join(str(e) for e in v)
            elif isinstance(v, bool):
                request[k] = int(v)
            elif isinstance(v, pydantic.BaseModel):
                request[k] = v.model_dump(exclude_none=True)
            elif isinstance(v, dict):
                request[k] = json.dumps(await self.validate(v))
            elif v is None:
                request.pop(k)
        return request


__all__ = ("TranslateFriendlyTypesRequestValidator",)
