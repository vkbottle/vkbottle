from .template import AbstractTemplate
from vkbottle.types.message import Message
from enum import Enum
import typing


class BotWorkSpace(Enum):
    DIALOG = 1
    CHAT = 2


async def echo_wrapper(ans: Message) -> str:
    return str(ans.text)


WorkSpace = typing.Tuple[BotWorkSpace]


class Echo(AbstractTemplate):
    wrapper: typing.Callable = echo_wrapper
    work_space: WorkSpace = ()

    def ready(
        self, workspace: WorkSpace = (BotWorkSpace.DIALOG, BotWorkSpace.CHAT)
    ) -> "Echo":
        self.bot.on.message_handler.add_handler(echo_wrapper)
        return self

    def run(self, skip_updates: bool = True, **kwargs):
        self.bot.run_polling(skip_updates=skip_updates, **kwargs)
