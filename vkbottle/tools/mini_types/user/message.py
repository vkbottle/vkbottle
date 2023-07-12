from typing import TYPE_CHECKING, List, Optional

from vkbottle.modules import pydantic
from vkbottle.tools.mini_types.base import BaseMessageMin

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI


from .foreign_message import ForeignMessageMin  # noqa: TCH001


class MessageMin(BaseMessageMin):
    user_id: Optional[int] = None
    reply_message: Optional["ForeignMessageMin"] = None
    fwd_messages: List["ForeignMessageMin"] = pydantic.Field(default_factory=list)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == self.user_id if self.mention else False

    @pydantic.root_validator(pre=True)
    def __foreign_messages(cls, values):
        foreign_messages = []
        if values.get("fwd_messages"):
            foreign_messages.extend(values["fwd_messages"])
        if values.get("reply_message"):
            foreign_messages.append(values["reply_message"])
        for foreign_message in foreign_messages:
            foreign_message["unprepared_ctx_api"] = values["unprepared_ctx_api"]
            foreign_message["replace_mention"] = values["replace_mention"]
            foreign_message["user_id"] = values.get("user_id")
        return values


MessageMin.update_forward_refs()


async def message_min(
    message_id: int,
    ctx_api: "ABCAPI",
    replace_mention: bool = True,
) -> "MessageMin":
    response = await ctx_api.messages.get_by_id(message_ids=[message_id])
    if not response.items:
        msg = f"Message with id {message_id} not found, perhaps it was deleted"
        raise ValueError(msg)
    message_object = response.items[0].dict()
    return MessageMin(
        **message_object,
        unprepared_ctx_api=ctx_api,
        replace_mention=replace_mention,
    )
