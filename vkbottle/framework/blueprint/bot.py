import typing

from vkbottle.api import exceptions, api
from vkbottle.framework.framework.branch import AbstractBranchGenerator, DictBranch
from vkbottle.framework.framework.extensions import AbstractExtension
from vkbottle.framework.framework.handler import (
    Handler,
    ErrorHandler,
    MiddlewareExecutor,
)

from .abc import AbstractBlueprint


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        # Main workers
        self.branch: typing.Optional[AbstractBranchGenerator] = DictBranch()
        self.middleware: MiddlewareExecutor = None
        self.on: Handler = Handler()
        self.error_handler = ErrorHandler()

        self.extension: AbstractExtension = None
        self.api: api.Api = None
        self._name = name or "Unknown"
        self._description = description or "Unknown"

    def create(
        self,
        *,
        familiar: typing.Tuple[AbstractBranchGenerator, AbstractExtension, api.Api],
    ):
        branch, extension, api_instance = familiar
        if not isinstance(self.branch, type(branch)):
            raise exceptions.VKError(
                f"All blueprints should have the same branch generative type ({self.name} "
                f"Blueprint, branch {self.branch.__name__} / familiar {branch.__name__}"
            )
        self.extension = extension
        self.api = api_instance
