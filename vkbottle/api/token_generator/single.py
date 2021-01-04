from .abc import ABCTokenGenerator


class SingleTokenGenerator(ABCTokenGenerator):
    def __init__(self, token: str):
        self.token = token

    async def get_token(self) -> str:
        return self.token
