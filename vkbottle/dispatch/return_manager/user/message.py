from typing import TYPE_CHECKING, Any, Union

from vkbottle.dispatch.return_manager.abc import BaseReturnManager

if TYPE_CHECKING:
    from vkbottle.tools.mini_types.user import MessageMin


class UserMessageReturnHandler(BaseReturnManager):
    @BaseReturnManager.instance_of(str)
    async def str_handler(self, value: str, message: "MessageMin", _: dict[str, Any]) -> None:
        await message.answer(value)

    @BaseReturnManager.instance_of((tuple, list))
    async def iter_handler(
        self, value: Union[tuple, list], message: "MessageMin", _: dict[str, Any]
    ) -> None:
        [await message.answer(str(e)) for e in value]

    @BaseReturnManager.instance_of(dict)
    async def dict_handler(
        self, value: dict[str, Any], message: "MessageMin", _: dict[str, Any]
    ) -> None:
        await message.answer(**value)


__all__ = ("UserMessageReturnHandler",)
