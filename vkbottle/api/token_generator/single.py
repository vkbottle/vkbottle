from .abc import ABCTokenGenerator


class SingleTokenGenerator(ABCTokenGenerator):
    def __init__(self, token: str):
        self.token = token

    async def get_token(self) -> str:
        return self.token

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
