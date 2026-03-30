import asyncio
from typing import TYPE_CHECKING

import pydantic
import vkbottle_types.objects
from vkbottle_types.objects import MessagesConversationMember

from vkbottle.modules import logger
from vkbottle.tools.mini_types.base import BaseMessageMin

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI

from .foreign_message import ForeignMessageMin, _foreign_messages


class MessageMin(BaseMessageMin):
    user_id: int | None = None
    reply_message: ForeignMessageMin | None = None  # type: ignore
    fwd_messages: list[ForeignMessageMin] = pydantic.Field(  # type: ignore
        default_factory=list[ForeignMessageMin],
    )
    _chat_members: list[MessagesConversationMember] | None = None

    __foreign_messages = pydantic.model_validator(mode="after")(_foreign_messages)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == self.user_id if self.mention else False


MessageMin.model_rebuild(_types_namespace=vars(vkbottle_types.objects) | locals())


async def message_min(
    message_id: int,
    ctx_api: "ABCAPI",
    replace_mention: bool = True,
) -> "MessageMin":
    response = await ctx_api.messages.get_by_id(message_ids=[message_id])

    if not response.items:
        logger.warning(f"Message with id {message_id} not found, perhaps it was deleted.")
        raise asyncio.CancelledError  # Cancel current task

    return MessageMin(
        **response.items[0].model_dump(),
        unprepared_ctx_api=ctx_api,
        replace_mention=replace_mention,
    )


__all__ = ("MessageMin",)
