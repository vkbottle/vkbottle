from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Final, List, Optional, Union

import pydantic
from vkbottle_types.objects import (
    MessagesForeignMessage,
    UsersUserFull,
)

from vkbottle.modules import json, logger

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

from .mention import Mention, replace_mention_validator
from .mixins import AttachmentMixin

PEER_ID_OFFSET: Final[int] = 2_000_000_000


class BaseForeignMessageMin(MessagesForeignMessage, AttachmentMixin, ABC):
    unprepared_ctx_api: Optional[Any] = None
    replace_mention: Optional[bool] = None
    _mention: Optional[Mention] = None

    __replace_mention = pydantic.model_validator(mode="after")(replace_mention_validator)  # type: ignore

    model_config = pydantic.ConfigDict(frozen=False)

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return self.unprepared_ctx_api  # type: ignore

    @property
    def mention(self) -> Optional[Mention]:
        """Returns `Mention` object if message contains mention,
        eg if message is `@username text` returns `Mention(id=123, text="text")`,
        also mention is automatically removes from message text"""
        if not self.replace_mention:
            logger.warning(
                "labeler.message_view.replace_mention is set to False, the mention will not be processed"
            )
            return None
        return self._mention

    @property
    @abstractmethod
    def is_mentioned(self) -> bool:
        """Returns True if current bot is mentioned in message"""

    async def get_user(self, raw_mode: bool = False, **kwargs) -> Union[UsersUserFull, dict]:
        raw_user = (await self.ctx_api.request("users.get", {"user_ids": self.from_id, **kwargs}))[
            "response"
        ][0]
        return raw_user if raw_mode else UsersUserFull(**raw_user)

    @property
    def chat_id(self) -> Optional[int]:
        return None if self.peer_id is None else self.peer_id - PEER_ID_OFFSET

    @property
    def message_id(self) -> Optional[int]:
        return self.conversation_message_id or self.id

    def get_message_id(self) -> Optional[int]:
        return self.id or self.conversation_message_id

    def get_payload_json(
        self,
        throw_error: bool = False,
        unpack_failure: Callable[[str], Union[dict, str]] = lambda payload: payload,
    ) -> Optional[Union[dict, str]]:
        if self.payload is None:
            return None

        try:
            return json.loads(self.payload)
        except (ValueError, TypeError) as e:
            if throw_error:
                raise e from None

        return unpack_failure(self.payload)


BaseForeignMessageMin.model_rebuild()


__all__ = ("BaseForeignMessageMin",)
