from collections.abc import Iterable
from typing import TYPE_CHECKING

from .consistent import ConsistentTokenGenerator
from .single import SingleTokenGenerator

if TYPE_CHECKING:
    from .abc import ABCTokenGenerator, Token


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
