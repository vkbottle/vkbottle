from vkbottle.api import UserApi
from vkbottle.framework.framework.handler import UserHandler


class UserBlueprint:

    _mode: int = 2

    def __init__(self, name: str = None, description: str = None):
        # Main workers
        self.on: UserHandler = UserHandler(self._mode)
        self.api: UserApi = UserApi.get_current()

        self._name = name
        self._description = description

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