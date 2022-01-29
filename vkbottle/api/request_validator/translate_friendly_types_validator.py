from pydantic import BaseModel

from vkbottle.modules import json

from .abc import ABCRequestValidator


class TranslateFriendlyTypesRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict) -> dict:
        for k, v in request.copy().items():
            if isinstance(v, list):
                request[k] = ",".join(str(e) for e in v)
            elif isinstance(v, bool):
                request[k] = int(v)
            elif isinstance(v, BaseModel):
                request[k] = v.json(exclude_none=True, encoder=json.dumps)
            elif isinstance(v, dict):
                request[k] = json.dumps(await self.validate(v))
            elif v is None:
                del request[k]
        return request
