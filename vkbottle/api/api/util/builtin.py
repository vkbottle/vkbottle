import random
import time
import math

from typing import List, Coroutine, Any
from vkbottle.utils.logger import logger

from vkbottle.api.api.util.token import AbstractTokenGenerator
from vkbottle.api.api.util.schema import TokenSchema


class RandomTokenGenerator(AbstractTokenGenerator):
    """
    RandomTokenGenerator allows to randomize taken tokens, works good if the amount of tokens is big
    """

    def __init__(self, tokens: List[str]):
        self.tokens = tokens

    async def get_token(self, *args, **kwargs) -> str:
        return random.choice(self.tokens)


class ConsistentTokenGenerator(AbstractTokenGenerator):
    """
    ConsistentTokenGenerator is the best choice to generate tokens and avoid limit errors
    """

    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.state = 0

    async def get_token(self, *args, **kwargs) -> str:
        index = self.state
        self.state = index + 1 if index + 1 < len(self.tokens) else 0
        return self.tokens[index]


class LimitedTokenGenerator(AbstractTokenGenerator):
    """
    LimitedTokenGenerator generates tokens with the fixed limit, it's aimed to efficiently avoid limit errors
    """

    def __init__(self, tokens: List[str], limit: int = 3):
        """
        :param tokens:
        :param limit: Fixed limit of availability of one token per second
        """
        self.tokens = tokens
        self.limit: int = limit
        self.last_time_stack = 0
        self.step: List[str] = []

    async def get_token(self, *args, **kwargs) -> str:
        time_stack = math.ceil(time.time())  # noqa: Accuracy to second

        if time_stack != self.last_time_stack:
            if self.last_time_stack == 0 or not len(self.step):
                self.step = self.token_sequence
        elif not len(self.step):
            logger.error(
                f"LimitedTokenGenerator is not able to avoid the limit because there are not enough tokens"
            )
            self.step = self.token_sequence

        self.last_time_stack = time_stack
        token = self.step.pop(0)
        return token

    @property
    def token_sequence(self) -> List[str]:
        return sorted(self.tokens * self.limit)


class ClassifiedTokenGenerator(AbstractTokenGenerator):
    """
    ClassifiedTokenGenerator is the best practice to work with API when all the tokens have different rights
    """

    def __init__(self, schema: TokenSchema):
        self.schema = schema

    @property
    def tokens(self):
        return []

    async def get_token(self, *args, **kwargs) -> Coroutine[Any, Any, str]:
        generator = self.schema.get_generator(*args, *kwargs)
        return generator.get_token(*args, **kwargs)


GENERATORS = {
    "consistent": ConsistentTokenGenerator,
    "random": RandomTokenGenerator,
    "limited": LimitedTokenGenerator,
    "classified": ClassifiedTokenGenerator,
}
