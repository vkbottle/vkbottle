from typing import Tuple

from vkbottle.api import UserApi
from vkbottle.framework.framework.branch import ABCBranchGenerator
from vkbottle.framework.framework.handler.user.handler import UserHandler
from vkbottle.utils.exceptions import VKError

from .abc import AbstractBlueprint


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        # Main workers
        self.on: UserHandler = UserHandler()
        self._name: str = name or "Unknown"
        self._description: str = description or "Unknown"

    def create(self, *, familiar: Tuple[ABCBranchGenerator, UserApi]):
        branch, api_instance = familiar
        if not isinstance(self.branch, type(branch)):
            raise VKError(
                0,
                f"All blueprints should have the same branch generative type ({self.name} "
                f"Blueprint, branch {self.branch} / familiar {branch}",
            )
        self.api = api_instance
