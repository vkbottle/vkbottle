from vkbottle.api import UserApi
from vkbottle.framework.framework.branch import AbstractBranchGenerator
from vkbottle.framework.framework.handler.user.handler import Handler
from vkbottle.utils.exceptions import VKError
from typing import Tuple
from .abc import AbstractBlueprint


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        # Main workers
        self.on: Handler = Handler()
        self._name: str = name or "Unknown"
        self._description: str = description or "Unknown"

    def create(
        self,
        *,
        familiar: Tuple[AbstractBranchGenerator, UserApi]
    ):
        branch, api_instance = familiar
        if not isinstance(self.branch, type(branch)):
            raise VKError(
                0,
                f"All blueprints should have the same branch generative type ({self.name} "
                f"Blueprint, branch {self.branch.__name__} / familiar {branch.__name__}",
            )
        self.api = api_instance
