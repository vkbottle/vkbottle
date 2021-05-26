import typing

from .abc import ABCFilter, ABCRule


class AndFilter(ABCFilter):
    def __init__(self, *rules: ABCRule):
        self._rules = rules

    async def check(self, event: typing.Any):
        context = {}

        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is False:
                return False
            elif isinstance(check_response, dict):
                context.update(check_response)

        return context

    @property
    def rules(self) -> typing.Iterable[ABCRule]:
        return self._rules


class OrFilter(ABCFilter):
    def __init__(self, *rules: ABCRule):
        self._rules = rules

    async def check(self, event: typing.Any):
        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is not False:
                return check_response
        return False

    @property
    def rules(self) -> typing.Iterable[ABCRule]:
        return self._rules
