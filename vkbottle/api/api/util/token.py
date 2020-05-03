from vkbottle.types.methods.access import APIAccessibility
from abc import ABC, abstractmethod
import typing
import warnings


class AbstractTokenGenerator(ABC):
    tokens_type: APIAccessibility = APIAccessibility.OPEN

    async def __aenter__(self, *args, **kwargs):
        return await self.get_token(*args, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} tokens_type={self.tokens_type} tokens_amount={self.__len__()}>"

    def __len__(self):
        tokens: typing.Optional[typing.Iterable[str]] = getattr(self, "tokens")
        if tokens is None:
            warnings.warn(
                f"Add property or name an attribute containing tokens '{self.__class__.__name__}.tokens'"
            )
            tokens = []
        return len(tokens)

    @abstractmethod
    async def get_token(self, *args, **kwargs) -> str:
        pass


class Token(AbstractTokenGenerator):
    def __init__(self, token: str):
        self.token = token

    @property
    def tokens(self) -> typing.Iterable[str]:
        return [self.token]

    async def get_token(self, *args, **kwargs) -> str:
        return self.token
