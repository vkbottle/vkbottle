import typing

from vkbottle.api.api import Api
from ...utils.exceptions import VKError
from vkbottle.framework.framework.branch import AbstractBranchGenerator
from vkbottle.framework.framework.extensions import AbstractExtension
from vkbottle.framework.framework.handler.handler import Handler
from .abc import AbstractBlueprint

Familiar = typing.Tuple[
    AbstractBranchGenerator, AbstractExtension, Api
]


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        self.on: Handler = Handler()
        self.extension: AbstractExtension = None
        self.data: dict = {}

        self._name = name or "Unknown"
        self._description = description or "Unknown"

    def create(
        self,
        *,
        familiar: Familiar,
        data: typing.Optional[dict] = None,
    ):
        branch, extension, api_instance = familiar
        if not isinstance(self.branch, type(branch)):
            raise VKError(
                0,
                f"All blueprints should have the same branch generative type ({self.name} "
                f"Blueprint, branch {self.branch.__name__} / familiar {branch.__name__}",
            )
        self.extension = extension
        self.api = api_instance
        if data is not None:
            self.data = data


bp = Blueprint()
