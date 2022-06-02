from typing import TYPE_CHECKING, List, Optional

from pydantic import root_validator

from ..base import BaseMessageMin
from .foreign_message import ForeignMessageMin

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI


class MessageMin(BaseMessageMin):
    user_id: Optional[int] = None
    reply_message: Optional["ForeignMessageMin"] = None
    fwd_messages: Optional[List["ForeignMessageMin"]] = []

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == self.user_id if self.mention else False

    @root_validator(pre=True)
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
    message_id: int, ctx_api: "ABCAPI", replace_mention: bool = True
) -> "MessageMin":
    message_object = (await ctx_api.request("messages.getById", {"message_ids": message_id}))[
        "response"
    ]["items"][0]
    return MessageMin(
        **message_object, unprepared_ctx_api=ctx_api, replace_mention=replace_mention
    )
