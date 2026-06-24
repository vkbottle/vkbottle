import asyncio
from typing import TYPE_CHECKING, Final

import pydantic
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

    @pydantic.model_validator(mode="after")
    def foreign_messages_model(self) -> "MessageMin":
        return _foreign_messages(self)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == self.user_id if self.mention else False


MessageMin.object_build(locals())

MESSAGE_FETCH_ATTEMPTS: Final = 3
MESSAGE_FETCH_RETRY_DELAY: Final = 0.1


async def message_min(
    message_id: int,
    ctx_api: "ABCAPI",
    replace_mention: bool = True,
    fetch_attempts: int = MESSAGE_FETCH_ATTEMPTS,
    fetch_retry_delay: float = MESSAGE_FETCH_RETRY_DELAY,
) -> "MessageMin":
    response = None

    for attempt in range(1, fetch_attempts + 1):
        response = await ctx_api.messages.get_by_id(message_ids=[message_id])

        if response.items:
            break

        if attempt < fetch_attempts:
            logger.debug(
                "Message with id {} not found on attempt {}/{}, retrying after {} seconds.",
                message_id,
                attempt,
                fetch_attempts,
                fetch_retry_delay,
            )
            await asyncio.sleep(fetch_retry_delay)

    if response is None or not response.items:
        logger.warning(f"Message with id {message_id} not found, perhaps it was deleted.")
        raise asyncio.CancelledError  # Cancel current task

    return MessageMin(
        **response.items[0].model_dump(),
        unprepared_ctx_api=ctx_api,
        replace_mention=replace_mention,
    )


__all__ = ("MessageMin",)
