from vkbottle.types.methods.access import APIAccessibility


class AbstractTokenGenerator:
    tokens_type: APIAccessibility = APIAccessibility.OPEN

    async def __aenter__(self, *args, **kwargs):
        return await self.get_token(*args, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} tokens_type={self.tokens_type}>"

    async def get_token(self, *args, **kwargs) -> str:
        ...


class Token(AbstractTokenGenerator):
    def __init__(self, token: str):
        self.token = token

    async def get_token(self, *args, **kwargs) -> str:
        return self.token
