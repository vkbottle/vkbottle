from .abc import ABCStorage
from vkbottle.tools.dev_tools.ctx_tool import BaseContext
import typing


class CtxStorage(ABCStorage, BaseContext):
    """ Context storage
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/tools/storage.md
    """

    storage: dict = {}

    def __init__(
        self, default: dict = None, force_reset: bool = False,
    ):

        default = default or {}
        if not self.get_instance() or force_reset:
            self.storage = default
            self.set_instance(self)

    def set(self, key: str, value: typing.Any) -> typing.NoReturn:
        current_storage = self.get_instance().storage
        current_storage[key] = value
        self.set_instance(CtxStorage(current_storage, True))

    def get(self, key: str) -> typing.Any:
        return self.get_instance().storage.get(key)

    def delete(self, key: str) -> typing.NoReturn:
        new_storage = self.get_instance().storage
        new_storage.pop(key)
        self.set_instance(CtxStorage(new_storage, True))

    def contains(self, key: str) -> bool:
        return key in self.get_instance().storage
