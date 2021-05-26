import typing

from vkbottle.tools.dev_tools.ctx_tool import BaseContext

from .abc import ABCStorage


class CtxStorage(ABCStorage, BaseContext):
    """ Context storage
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/tools/storage.md
    """

    storage: dict = {}

    def __init__(
        self, default: dict = None, force_reset: bool = False,
    ):

        default = default or {}
        if not self.get_instance() or force_reset:
            self.storage = default
            self.set_instance(self)

    def set(self, key: typing.Hashable, value: typing.Any) -> None:
        current_storage = self.get_instance().storage
        current_storage[key] = value
        self.set_instance(CtxStorage(current_storage, True))

    def get(self, key: typing.Hashable) -> typing.Any:
        return self.get_instance().storage.get(key)

    def delete(self, key: typing.Hashable) -> None:
        new_storage = self.get_instance().storage
        new_storage.pop(key)
        self.set_instance(CtxStorage(new_storage, True))

    def contains(self, key: typing.Hashable) -> bool:
        return key in self.get_instance().storage
