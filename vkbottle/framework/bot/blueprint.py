import typing

from vkbottle.api import exceptions, api
from vkbottle.framework.framework.branch import AbstractBranchGenerator, DictBranch
from vkbottle.framework.framework.extensions import AbstractExtension
from vkbottle.framework.framework.handler import Handler, ErrorHandler, MiddlewareExecutor
from .builtin import DEFAULT_BLUEPRINT


class Blueprint:
    def __init__(self, name: str = None, description: str = None):
        # Main workers
        self.branch: typing.Optional[AbstractBranchGenerator] = DictBranch()
        self.middleware: MiddlewareExecutor = None
        self.on: Handler = Handler()
        self.error_handler = ErrorHandler()

        self.extension: AbstractExtension = None
        self.api: api.Api = None
        self._name = name or DEFAULT_BLUEPRINT[0]
        self._description = description or DEFAULT_BLUEPRINT[1]

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description: str):
        self._description = new_description
