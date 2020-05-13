import typing
from ..rule import AbstractRule, RuleExecute


class AbstractFilter:
    def __init__(self, *rules: AbstractRule):
        self.rules: typing.Tuple[AbstractRule] = rules
        self.context = RuleExecute()

    def create(self, *args, **kwargs):
        pass

    async def __call__(self, event) -> bool:
        self.__init_subclass__()
        return await self.check(event)

    async def check(self, event) -> bool:
        ...

    def __repr__(self):
        return (
            f"<Filter {self.__class__.__qualname__} "
            f"rules={(rule.__class__.__name__ for rule in self.rules)} "
            f"context={self.context}>"
        )
