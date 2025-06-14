from typing import TYPE_CHECKING, List, Optional

import pydantic
from vkbottle_types.events.bot_events import MessageNew

from vkbottle.tools.mini_types.base import BaseMessageMin

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI


from vkbottle_types.objects import ClientInfoForBots, MessagesConversationMember

from vkbottle.modules import logger

from .foreign_message import ForeignMessageMin, _foreign_messages


class MessageMin(BaseMessageMin):
    group_id: Optional[int] = None
    client_info: Optional[ClientInfoForBots] = None
    reply_message: Optional[ForeignMessageMin] = None
    fwd_messages: List[ForeignMessageMin] = pydantic.Field(
        default_factory=list[ForeignMessageMin],
    )
    _is_full: Optional[bool] = None
    _chat_members: Optional[List[MessagesConversationMember]] = None

    __foreign_messages = pydantic.model_validator(mode="after")(_foreign_messages)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == -self.group_id if (self.mention and self.group_id) else False

    async def get_full_message(self) -> "BaseMessageMin":
        if self._is_full:
            return self
        message = (
            await self.ctx_api.messages.get_by_conversation_message_id(
                peer_id=self.peer_id,
                conversation_message_ids=[self.conversation_message_id],  # type: ignore
            )
        ).items[0]
        self.__dict__.update(message.__dict__)
        super().__init__(**self.model_dump())
        self.__dict__["_is_full"] = True
        if self.is_cropped:
            self.__dict__["is_cropped"] = False
        return self

    def get_attachment_strings(self) -> Optional[List[str]]:
        if self.attachments is None:
            return None
        if (
            not self.id
            and not self._is_full
            and any(
                getattr(attachment, attachment.type.value).access_key
                for attachment in self.attachments
            )
        ):
            logger.warning(
                "Some attachments may does't work because of wrong access_key. "
                "Use .get_full_message() to update message and fix this issue."
            )
        if self.is_cropped:
            logger.warning(
                "Some attachments may doesn't included because message is cropped. "
                "Use .get_full_message() to update message and fix this issue."
            )
        return super().get_attachment_strings()


def message_min(event: dict, ctx_api: "ABCAPI", replace_mention: bool = True) -> "MessageMin":
    update = MessageNew.from_dict(event)

    if update.object.message is None:
        msg = "Please set longpoll to latest version"
        raise RuntimeError(msg)

    return MessageMin(
        **update.object.message.to_dict(),
        client_info=update.object.client_info,
        group_id=update.group_id,
        replace_mention=replace_mention,
        unprepared_ctx_api=ctx_api,
    )


__all__ = ("MessageMin",)
