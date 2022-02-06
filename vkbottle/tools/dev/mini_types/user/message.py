from typing import TYPE_CHECKING, List, Optional

from ..base import BaseMessageMin

if TYPE_CHECKING:
    from vkbottle_types.responses.messages import MessagesSendUserIdsResponseItem

    from vkbottle.api import ABCAPI


class MessageMin(BaseMessageMin):
    user_id: Optional[int] = None

    @property
    def is_mentioned(self) -> bool:
        if not self.mention:
            return False
        return self.mention.id == self.user_id

    async def reply(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        **kwargs,
    ) -> "MessagesSendUserIdsResponseItem":
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        data["reply_to"] = self.id

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
            forward_message_ids = [self.id]

        data["forward_messages"] = forward_message_ids

        return await self.answer(**data)


MessageMin.update_forward_refs()


async def message_min(message_id: int, ctx_api: "ABCAPI") -> "MessageMin":
    message_object = (await ctx_api.request("messages.getById", {"message_ids": message_id}))[
        "response"
    ]["items"][0]
    message = MessageMin(**message_object)
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
