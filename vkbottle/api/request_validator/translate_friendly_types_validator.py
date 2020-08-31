from .abc import ABCRequestValidator


class TranslateFriendlyTypesRequestValidator(ABCRequestValidator):
    async def validate(self, response: dict) -> dict:
        for k, v in response.items():
            # translate python-list to vk array-like type
            if isinstance(v, list):
                response[k] = ",".join(str(e) for e in v)
        return response
