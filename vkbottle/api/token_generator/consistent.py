import itertools
from typing import Iterable

from .abc import ABCTokenGenerator


class ConsistentTokenGenerator(ABCTokenGenerator):
    def __init__(self, tokens: Iterable[str]):
        self.tokens = itertools.cycle(tokens)

    async def get_token(self) -> str:
        return next(self.tokens)
