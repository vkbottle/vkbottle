import typing

from vkbottle.api import api
from ...utils import exceptions
from vkbottle.framework.framework.branch import AbstractBranchGenerator, DictBranch
from vkbottle.framework.framework.extensions import AbstractExtension
from vkbottle.framework.framework.handler import MiddlewareExecutor
from vkbottle.framework.framework.error_handler import (
    VKErrorHandler,
    DefaultErrorHandler,
)
from vkbottle.framework.framework.handler.handler import Handler
from .abc import AbstractBlueprint


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        # Main workers
        self.branch: typing.Optional[AbstractBranchGenerator] = DictBranch()
        self.middleware: MiddlewareExecutor = MiddlewareExecutor()
        self.on: Handler = Handler()
        self.error_handler: VKErrorHandler = DefaultErrorHandler()

        self.extension: AbstractExtension = None
        self.api: api.Api = None
        self._name = name or "Unknown"
        self._description = description or "Unknown"
        self.data: dict = {}

    def create(
        self,
        *,
        familiar: typing.Tuple[AbstractBranchGenerator, AbstractExtension, api.Api],
        data: typing.Optional[dict] = None,
    ):
        branch, extension, api_instance = familiar
        if not isinstance(self.branch, type(branch)):
            raise exceptions.VKError(
                0,
                f"All blueprints should have the same branch generative type ({self.name} "
                f"Blueprint, branch {self.branch.__name__} / familiar {branch.__name__}",
            )
        self.extension = extension
        self.api = api_instance
        if data is not None:
            self.data = data
