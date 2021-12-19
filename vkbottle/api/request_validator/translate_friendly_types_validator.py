from pydantic import BaseModel

from .abc import ABCRequestValidator
from vkbottle.modules import json


class TranslateFriendlyTypesRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict) -> dict:
        for k, v in request.items():
            # translate python-list to vk array-like type
            if isinstance(v, list):
                request[k] = ",".join(str(e) for e in v)
            elif isinstance(v, bool):
                request[k] = int(v)
            elif isinstance(v, BaseModel):
                request[k] = v.json(exclude_none=True, encoder=json.dumps)
        return request
