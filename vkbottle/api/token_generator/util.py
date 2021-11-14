from typing import Iterable

from .abc import ABCTokenGenerator, Token
from .consistent import ConsistentTokenGenerator
from .single import SingleTokenGenerator


def get_token_generator(token: "Token") -> "ABCTokenGenerator":
    """Converts token shortcuts to generators
    >>> get_token_generator("abc123") # <SingleTokenGenerator>
    >>> get_token_generator(["abc123", "def456"]) # <ConsistentTokenGenerator>
    >>> get_token_generator(ConsistentTokenGenerator(["abc123", "def456"])) # <ConsistentTokenGenerator>
    """
    if isinstance(token, str):
        return SingleTokenGenerator(token)
    elif isinstance(token, Iterable):
        return ConsistentTokenGenerator(token)
    return token
