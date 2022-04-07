from typing import TYPE_CHECKING, List, Optional

from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types.objects import ClientInfoForBots, MessagesForward

from ..base import BaseMessageMin
from vkbottle.modules import logger

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

    async def get_full_message(self) -> "MessageMin":
        if self.is_cropped is None and self.id:
            return self
        message = (
            await self.ctx_api.messages.get_by_conversation_message_id(
                peer_id=self.peer_id,
                conversation_message_ids=[self.conversation_message_id],  # type: ignore
            )
        ).items[0]
        if self.is_cropped:
            message.is_cropped = False
        for k, v in message.__dict__.items():
            self.__dict__[k] = v
        return self

    def get_attachments(self) -> List[str]:
        if not self.attachments:
            return []
        if not self.id and any(
            getattr(attachment, attachment.type.value).access_key
            for attachment in self.attachments
        ):
            logger.warning(
                (
                    "Some attachments may does't work because of wrong access_key. "
                    "Use .get_full_message() to update message and fix this issue."
                )
            )
        if self.is_cropped:
            logger.warning(
                (
                    "Some attachments may doesn't included because message is cropped. "
                    "Use .get_full_message() to update message and fix this issue."
                )
            )
        attachments = []
        for attachment in self.attachments:
            attachment_type = attachment.type.value
            attachment_object = getattr(attachment, attachment_type)
            if not hasattr(attachment_object, "id") or not hasattr(attachment_object, "owner_id"):
                continue
            attachment_string = (
                f"{attachment_type}{attachment_object.owner_id}_{attachment_object.id}"
            )
            if hasattr(attachment_object, "access_key"):
                attachment_string += f"_{attachment_object.access_key}"
            attachments.append(attachment_string)
        return attachments

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
