import typing

from .from_func_handler import FromFuncHandler

if typing.TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.tools.mini_types.base import BaseMessageMin


class MessageReplyHandler(FromFuncHandler["BaseMessageMin"]):
    def __init__(
        self,
        text: str,
        *rules: "ABCRule[BaseMessageMin]",
        is_blocking: bool = True,
        as_reply: bool = False,
        **default_params: typing.Any,
    ) -> None:
        super().__init__(self.reply_handler, *rules, blocking=is_blocking)
        self.text = text
        self.as_reply = as_reply
        self.default_params = default_params

    async def reply_handler(self, message: "BaseMessageMin") -> None:
        params = {"message": self.text, "random_id": 0, **self.default_params}
        method = message.reply if self.as_reply else message.answer
        await method(**params)  # type: ignore


__all__ = ("MessageReplyHandler",)
