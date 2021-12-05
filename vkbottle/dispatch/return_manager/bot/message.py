from typing import TYPE_CHECKING, Union

from vkbottle.dispatch.return_manager.abc import BaseReturnManager

if TYPE_CHECKING:
    from vkbottle.tools.dev.mini_types.bot import MessageMin


class BotMessageReturnHandler(BaseReturnManager):
    @BaseReturnManager.instance_of(str)
    async def str_handler(self, value: str, message: "MessageMin", _: dict):
        await message.answer(value)

    @BaseReturnManager.instance_of((tuple, list))
    async def iter_handler(self, value: Union[tuple, list], message: "MessageMin", _: dict):
        [await message.answer(str(e)) for e in value]

    @BaseReturnManager.instance_of(dict)
    async def dict_handler(self, value: dict, message: "MessageMin", _: dict):
        await message.answer(**value)
