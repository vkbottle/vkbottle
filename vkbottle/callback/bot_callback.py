from random import choice
from string import ascii_lowercase
from typing import TYPE_CHECKING, Any

from typing_extensions import Self

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
        url: str | None = None,
        title: str | None = None,
        secret_key: str | None = None,
        api: "ABCAPI | None" = None,
        group_id: int | None = None,
        error_handler: "ABCErrorHandler | None" = None,
    ) -> None:
        self.url = url
        self.title = title
        self.secret_key = secret_key or self._generate_secret_key()
        self._api = api
        self.group_id = group_id
        self.error_handler = error_handler or ErrorHandler()  # type: ignore

    def get_secret_key(self) -> str:
        return self.secret_key

    def _generate_secret_key(self) -> str:
        return "".join(choice(ascii_lowercase) for _ in range(32))

    async def setup_group_id(self):
        if self.group_id is None:
            self.group_id = (await self.api.request("groups.getById", {}))["response"]["groups"][
                0
            ]["id"]

    async def find_server_id(self) -> int | None:
        servers = await self.get_callback_servers()
        if servers:
            return next((server["id"] for server in servers if server["url"] == self.url), None)
        return None

    async def add_callback_server(self) -> int:
        logger.debug("Adding callback server...")
        data = {
            "group_id": self.group_id,
            "url": self.url,
            "title": self.title,
            "secret_key": self.secret_key,
        }
        return (await self.api.request("groups.addCallbackServer", data))["response"]["server_id"]

    async def delete_callback_server(self, server_id: int) -> None:
        logger.debug("Delete callback server...")
        await self.api.request(
            "groups.deleteCallbackServer", {"group_id": self.group_id, "server_id": server_id}
        )

    async def edit_callback_server(self, server_id: int, secret_key: str | None = None) -> None:
        logger.debug("Editing callback server...")
        data = {
            "group_id": self.group_id,
            "server_id": server_id,
            "url": self.url,
            "title": self.title,
            "secret_key": self.secret_key,
        }

        if secret_key is not None:
            data["secret_key"] = secret_key
        await self.api.request("groups.editCallbackServer", data)

    async def get_callback_confirmation_code(self) -> str:
        logger.debug("Getting callback confirmation code...")
        return (
            await self.api.request(
                "groups.getCallbackConfirmationCode",
                {
                    "group_id": self.group_id,
                },
            )
        )["response"]["code"]

    async def get_callback_servers(
        self,
        servers_ids: list[int] | None = None,
    ) -> list[dict[str, Any]]:
        logger.debug("Getting callback servers...")
        data: dict[str, Any] = {"group_id": self.group_id}
        if servers_ids is not None:
            data["server_ids"] = ",".join(map(str, servers_ids))
        return (await self.api.request("groups.getCallbackServers", data))["response"]["items"]

    async def get_callback_settings(self, server_id: int) -> dict[str, bool]:
        logger.debug("Getting callback settings...")
        return (
            await self.api.request(
                "groups.getCallbackSettings", {"group_id": self.group_id, "server_id": server_id}
            )
        )["response"]["events"]

    async def set_callback_settings(
        self,
        server_id: int,
        params: dict[str, bool] | None = None,
    ) -> None:
        """Search values in https://dev.vk.ru/method/groups.getCallbackSettings"""

        logger.debug("Setting callback settings...")

        data = {"group_id": self.group_id, "server_id": server_id}

        if params is not None:
            for k, v in params.items():
                data[k] = v  # noqa: PERF403
        await self.api.request("groups.setCallbackSettings", data)

    def construct(
        self,
        api: "ABCAPI",
        error_handler: "ABCErrorHandler | None" = None,
    ) -> Self:
        self._api = api
        if error_handler is not None:
            self.error_handler = error_handler
        return self

    @property
    def api(self) -> "ABCAPI":
        if self._api is None:
            msg = "You must construct callback with API before try to access api property of Callback"
            raise NotImplementedError(msg)
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI") -> None:
        self._api = new_api
