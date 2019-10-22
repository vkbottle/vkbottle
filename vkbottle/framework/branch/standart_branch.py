class Branch:
    branch_name: str
    branch_kwargs: dict

    def __init__(self, branch_name: str, **pass_to_branch):
        self.branch_name = branch_name
        self.branch_kwargs = pass_to_branch


class ExitBranch:
    def __init__(self):
        pass
