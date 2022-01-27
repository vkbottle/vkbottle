from random import choice
from string import ascii_lowercase
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from vkbottle.exception_factory import ErrorHandler
from vkbottle.modules import logger

from .abc import ABCCallback

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class BotCallback(ABCCallback):
    """Bot Callback class"""

    def __init__(
        self,
        url: Optional[str] = None,
        title: Optional[str] = None,
        secret_key: Optional[str] = None,
        api: Optional["ABCAPI"] = None,
        group_id: Optional[int] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ):
        self.url = url
        self.title = title
        self.secret_key = secret_key or self._generate_secret_key()
        self._api = api
        self.group_id = group_id
        self.error_handler = error_handler or ErrorHandler()

    def _generate_secret_key(self) -> str:
        return "".join(choice(ascii_lowercase) for _ in range(30))

    def get_secret_key(self) -> str:
        return self.secret_key

    async def add_callback_server(self):
        logger.debug("Adding callback server...")
        data = {
            "group_id": self.group_id,
            "url": self.url,
            "title": self.title,
            "secret_key": self.secret_key,
        }
        await self.api.request("groups.addCallbackServer", data)

    async def delete_callback_server(self, server_id: int):
        logger.debug("Delete callback server...")
        await self.api.request(
            "groups.deleteCallbackServer", {"group_id": self.group_id, "server_id": server_id}
        )

    async def edit_callback_server(self, server_id: int, secret_key: Optional[str] = None):
        logger.debug("Editing callback server...")
        data = {
            "group_id": self.group_id,
            "server_id": server_id,
            "url": self.url,
            "title": self.title,
            "secret_key": self._generate_secret_key(),
        }
        if secret_key is not None:
            data.update({"secret_key": secret_key})
        await self.api.request("groups.editCallbackServer", data)

    async def get_callback_confirmation_code(self) -> str:
        logger.debug("Getting callback confirmation code...")
        if self.group_id is None:
            self.group_id = (await self.api.request("groups.getById", {}))["response"][0]["id"]
        return (
            await self.api.request(
                "groups.getCallbackConfirmationCode",
                {
                    "group_id": self.group_id,
                },
            )
        )["response"]["code"]

    async def get_callback_servers(
        self, servers_ids: Optional[List[int]] = None
    ) -> List[Dict[int, Dict[str, Any]]]:
        data: Dict[str, Any] = {"group_id": self.group_id}
        if servers_ids is not None:
            data.update({"server_ids": ",".join(map(str, servers_ids))})
        return (await self.api.request("groups.getCallbackServers", data))["response"]["items"]

    async def get_callback_settings(self, server_id: int) -> dict:
        return (
            await self.api.request(
                "groups.getCallbackSettings", {"group_id": self.group_id, "server_id": server_id}
            )
        )["response"]["events"]

    async def set_callback_settings(
        self, server_id: int, params: Optional[Dict[str, bool]] = None
    ):
        """Search values in https://dev.vk.com/method/groups.getCallbackSettings"""

        data = {"group_id": self.group_id, "server_id": server_id}

        if params is not None:
            for k, v in params.items():
                data.update({k: v})
        await self.api.request("groups.setCallbackSettings", data)

    def construct(
        self, api: "ABCAPI", error_handler: Optional["ABCErrorHandler"] = None
    ) -> "BotCallback":
        self._api = api
        if error_handler is not None:
            self.error_handler = error_handler
        return self

    @property
    def api(self) -> "ABCAPI":
        if self._api is None:
            raise NotImplementedError(
                "You must construct polling with API before try to access api property of Polling"
            )
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI"):
        self._api = new_api
