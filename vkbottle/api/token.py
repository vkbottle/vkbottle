from ..utils import ContextInstanceMixin
import typing


class TokenQueue(ContextInstanceMixin):
    tokens: typing.List[str] = []
    index: int = 0

    def __init__(self, token: str):
        self.tokens.append(token)

    def extend(self, *tokens):
        self.tokens.extend(tokens)

    def get(self):
        token = self.tokens[self.index]
        self.index = self.index + 1 if self.index + 1 < len(self.tokens) else 0
        return token
