from typing import TYPE_CHECKING, List, Optional

from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types.objects import ClientInfoForBots, MessagesForward

from ..base import BaseMessageMin

if TYPE_CHECKING:
    from vkbottle_types.responses.messages import MessagesSendUserIdsResponseItem

    from vkbottle.api import ABCAPI


class MessageMin(BaseMessageMin):
    group_id: Optional[int] = None
    client_info: Optional["ClientInfoForBots"] = None

    @property
    def is_mentioned(self) -> bool:
        if not (self.mention and self.group_id):
            return False
        return self.mention.id == -self.group_id

    async def reply(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        **kwargs,
    ) -> "MessagesSendUserIdsResponseItem":
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        data["forward"] = MessagesForward(
            conversation_message_ids=[self.conversation_message_id],  # type: ignore
            peer_id=self.peer_id,
            is_reply=True,
        ).json()

        return await self.answer(**data)

    async def forward(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        forward_message_ids: Optional[List[int]] = None,
        **kwargs,
    ) -> "MessagesSendUserIdsResponseItem":
        locals().update(kwargs)

        data = {
            k: v
            for k, v in locals().items()
            if k not in ("self", "kwargs", "forward_message_ids") and v is not None
        }
        if not forward_message_ids:
            forward_message_ids = [self.conversation_message_id]  # type: ignore
        data["forward"] = MessagesForward(
            conversation_message_ids=forward_message_ids, peer_id=self.peer_id
        ).json()

        return await self.answer(**data)


def message_min(event: dict, ctx_api: "ABCAPI") -> "MessageMin":
    update = MessageNew(**event)

    if update.object.message is None:
        raise RuntimeError("Please set longpoll to latest version")

    message = MessageMin(
        **update.object.message.dict(),
        client_info=update.object.client_info,
        group_id=update.group_id,
    )
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
