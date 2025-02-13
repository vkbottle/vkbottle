import itertools
from collections.abc import Iterable

from .abc import ABCTokenGenerator


class ConsistentTokenGenerator(ABCTokenGenerator):
    def __init__(self, tokens: Iterable[str]):
        self.tokens = itertools.cycle(tokens)

    async def get_token(self) -> str:
        return next(self.tokens)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
