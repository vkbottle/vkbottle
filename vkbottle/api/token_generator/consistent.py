import itertools
from typing import List

from .abc import ABCTokenGenerator


class ConsistentTokenGenerator(ABCTokenGenerator):
    def __init__(self, tokens: List[str]):
        self.tokens = itertools.cycle(tokens)

    async def get_token(self) -> str:
        return next(self.tokens)
