import typing
from ..rule import AbstractMessageRule


class Branch:
    branch_name: str
    branch_kwargs: dict

    def __init__(self, branch_name: str, **pass_to_branch):
        self.branch_name = branch_name
        self.branch_kwargs = pass_to_branch


class ExitBranch:
    def __init__(self):
        pass


def rule_disposal(*rules: AbstractMessageRule):
    disposal = []

    def wrapper(func):
        for rule in rules:
            rule.create(func)
            disposal.append(rule)
        return func, disposal

    return wrapper
