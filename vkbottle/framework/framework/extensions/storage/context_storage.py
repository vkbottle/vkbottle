from .abc import ABCStorage
from vkbottle.utils import ContextInstanceMixin
import typing


class CtxStorage(ABCStorage, ContextInstanceMixin):
    storage: dict = {}

    def __init__(self, default: dict = None, force_reset: bool = False):
        default = default or {}
        if not self.get_current() or force_reset:
            self.storage = default
            self.set_current(self)

    def set(self, key: str, value: typing.Any) -> None:
        current_storage = self.get_current().storage
        current_storage[key] = value
        self.set_current(CtxStorage(current_storage, True))

    def get(self, key: str) -> typing.Any:
        return self.get_current().storage.get(key)

    def delete(self, key: str) -> None:
        new_storage = self.get_current().storage
        new_storage.pop(key)
        self.set_current(CtxStorage(new_storage, True))

    def contains(self, key: str) -> bool:
        return key in self.get_current().storage
