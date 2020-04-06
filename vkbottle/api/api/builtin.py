import typing
import random
import time
import math
from vkbottle.utils.logger import logger
from .token import AbstractTokenGenerator
from .schema import TokenSchema


class RandomTokenGenerator(AbstractTokenGenerator):
    """
    RandomTokenGenerator allows to randomize taken tokens, works good if the amount of tokens is big
    """

    def __init__(self, tokens: typing.List[str]):
        self.tokens = tokens

    async def get_token(self, *args, **kwargs) -> str:
        return random.choice(self.tokens)


class ConsistentTokenGenerator(AbstractTokenGenerator):
    """
    ConsistentTokenGenerator is the best choice to generate tokens and avoid limit errors
    """

    def __init__(self, tokens: typing.List[str]):
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

    def __init__(self, tokens: typing.List[str], limit: int = 3):
        """
        :param tokens:
        :param limit: Fixed limit of availability of one token per second
        """
        self.tokens = tokens
        self.limit: int = limit
        self.state: typing.Tuple[int] = (0, 0)

    async def get_token(self, *args, **kwargs) -> str:
        index = self.state[1]
        timestack = math.floor(time.time())  # noqa: Accuracy to second
        if timestack == self.state[0]:
            if index + 1 > self.limit or index + 1 < len(self.tokens):
                logger.error(
                    f"LimitedTokenGenerator is not able to avoid the limit because there are not enough tokens ({index + 1} \"{self.tokens[index][:11]}...\")"
                )
                self.state = (timestack, 0)
            else:
                self.state = (timestack, index + 1)
        else:
            self.state = (timestack, 0)
        return self.tokens[index]


class ClassifiedTokenGenerator(AbstractTokenGenerator):
    """
    ClassifiedTokenGenerator is the best practice to work with API when all the tokens have different rights
    """

    def __init__(self, schema: TokenSchema):
        self.schema = schema

    async def get_token(self, *args, **kwargs) -> str:
        generator = self.schema.get_generator(*args, *kwargs)
        return generator.get_token(*args, **kwargs)


GENERATORS = {
    "consistent": ConsistentTokenGenerator,
    "random": RandomTokenGenerator,
    "limited": LimitedTokenGenerator,
    "classified": ClassifiedTokenGenerator,
}
