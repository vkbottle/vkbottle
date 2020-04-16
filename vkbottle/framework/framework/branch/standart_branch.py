from vkbottle.framework.framework.rule import AbstractMessageRule


class Branch:
    branch_name: str
    branch_kwargs: dict

    def __init__(self, branch_name: str, **pass_to_branch):
        self.branch_name = branch_name
        self.branch_kwargs = pass_to_branch


class ExitBranch:
    def __init__(self):
        pass


class ImmutableBranchData:
    def __init__(self, name: str, **kwargs):
        self.name: str = name
        self.data = kwargs

    def __call__(self) -> dict:
        return {"name": self.name, **self.data}

    def __repr__(self):
        return f"<Branch ImmutableBranchData name={self.name} data={self.data}>"


def rule_disposal(*rules: AbstractMessageRule):
    disposal = []

    def wrapper(func):
        for rule in rules:
            rule.create(func)
            disposal.append(rule)
        return func, disposal

    return wrapper
