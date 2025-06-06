from collections.abc import Hashable
from typing import Any, Optional

from vkbottle.tools.ctx_tool import BaseContext

from .abc import ABCStorage


class CtxStorage(ABCStorage, BaseContext):
    """Context storage
    Documentation: https://vkbottle.rtfd.io/ru/latest/tools/storage
    """

    storage: dict

    def __init__(
        self,
        default: Optional[dict] = None,
        force_reset: bool = False,
    ):
        if not self.get_instance() or force_reset:
            default = default or {}
            self.storage = default
            self.set_instance(self)

    def set(self, key: Hashable, value: Any) -> None:
        current_storage = self.get_instance().storage
        current_storage[key] = value
        self.set_instance(CtxStorage(current_storage, True))

    def get(self, key: Hashable) -> Any:
        return self.get_instance().storage.get(key)

    def delete(self, key: Hashable) -> None:
        new_storage = self.get_instance().storage
        new_storage.pop(key)
        self.set_instance(CtxStorage(new_storage, True))

    def contains(self, key: Hashable) -> bool:
        return key in self.get_instance().storage
