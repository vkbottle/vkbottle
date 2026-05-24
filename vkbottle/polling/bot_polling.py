from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiohttp import ClientTimeout
from typing_extensions import Self

from vkbottle.exception_factory import ErrorHandler
from vkbottle.modules import json, logger

from .base import BasePolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class BotPolling(BasePolling):
    """Bot Polling class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/polling
    """

    def __init__(
        self,
        api: "ABCAPI | None" = None,
        group_id: int | None = None,
        wait: int | None = None,
        rps_delay: int | None = None,
        skip_old_events: bool = True,
        error_handler: "ABCErrorHandler | None" = None,
    ) -> None:
        self._api = api
        self.error_handler = error_handler or ErrorHandler()
        self.group_id = group_id
        self.wait = min(wait or 25, 90)
        self.rps_delay = rps_delay or 0
        self.skip_old_events = skip_old_events

    @property
    def ts_state_path(self) -> Path:
        if self.group_id is None:
            msg = "Bot polling state path is unavailable before group_id is resolved"
            raise RuntimeError(msg)
        return Path.cwd() / ".vkbottle" / "bot-polling" / f"{self.group_id}.json"

    def restore_server_ts(self, server: dict[str, Any]) -> dict[str, Any]:
        if self.skip_old_events:
            return server

        try:
            with self.ts_state_path.open(encoding="utf-8") as f:
                state = json.load(f)
        except FileNotFoundError:
            return server
        except (OSError, TypeError, ValueError) as e:
            logger.warning("Unable to load bot polling state from {}: {}", self.ts_state_path, e)
            return server

        ts = state.get("ts")
        if ts is None:
            return server

        logger.info("Restoring bot polling ts {} from {}", ts, self.ts_state_path)
        server["ts"] = ts
        return server

    def save_server_ts(self, server: dict[str, Any]) -> None:
        path = self.ts_state_path
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".tmp")
        state = {"ts": server["ts"]}

        try:
            with temp_path.open("w", encoding="utf-8") as f:
                json.dump(state, f)
            temp_path.replace(path)
        except OSError as e:
            logger.warning("Unable to save bot polling state to {}: {}", path, e)

    async def get_event(self, server: dict[str, Any]) -> dict[str, Any]:
        # sourcery skip: use-fstring-for-formatting
        logger.debug("Making long request to get event with longpoll...")
        return await self.api.http_client.request_json(
            url=server["server"],
            method="POST",
            params={
                "act": "a_check",
                "key": server["key"],
                "ts": server["ts"],
                "wait": self.wait,
                "rps_delay": self.rps_delay,
            },
            timeout=ClientTimeout(total=self.wait + 10),
        )

    async def get_server(self) -> dict[str, Any]:
        logger.debug("Getting polling server...")
        if self.group_id is None:
            response = (await self.api.request("groups.getById", {}))["response"]
            if not response.get("groups", []):
                msg = "Unable to get group id for bot polling. Perhaps you are using a user access token?"
                raise RuntimeError(msg)

            self.group_id = response["groups"][0]["id"]

        return (
            await self.api.request(
                "groups.getLongPollServer",
                {"group_id": self.group_id},
            )
        )["response"]

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
            msg = (
                "You must construct polling with API before try to access api property of Polling"
            )
            raise NotImplementedError(msg)
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI") -> None:
        self._api = new_api


__all__ = ("BotPolling",)
