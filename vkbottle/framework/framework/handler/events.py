import typing
from abc import ABC

from vkbottle.framework.framework.rule import EventRule


class ABCEvents(ABC):
    rules: typing.List[EventRule] = list()

    def __call__(self, *events):
        def decorator(func):
            rule = EventRule(list(events))
            rule.create(func)
            self.rules.append(rule)
            return func

        return decorator

    def rule(self, rule):
        def decorator(func):
            rule.create(func)
            self.rules.append(rule)
            return func

        return decorator
