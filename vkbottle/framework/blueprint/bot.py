import typing

from vkbottle.api.api import Api
from vkbottle.framework.framework.branch import ABCBranchGenerator
from vkbottle.framework.framework.extensions import AbstractExtension
from vkbottle.framework.framework.handler.bot.handler import BotHandler

from ...utils.exceptions import VKError
from .abc import AbstractBlueprint

Familiar = typing.Tuple[ABCBranchGenerator, AbstractExtension, Api]


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        self.on: BotHandler = BotHandler()
        self.extension: AbstractExtension = None
        self.data: dict = {}

        self._name = name or "Unknown"
        self._description = description or "Unknown"

    def create(
        self, *, familiar: Familiar, data: typing.Optional[dict] = None,
    ):
        branch, extension, api_instance = familiar
        if not isinstance(self.branch, type(branch)):
            raise VKError(
                0,
                f"All blueprints should have the same branch generative type ({self.name} "
                f"Blueprint, branch {self.branch} / familiar {branch}",
            )
        self.extension = extension
        self.api = api_instance
        if data is not None:
            self.data = data


bp = Blueprint()
