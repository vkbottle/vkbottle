from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class ABCCallback(ABC):
    """
    Abstract Callback class
    """

    @abstractmethod
    def get_secret_key(self) -> str:
        pass

    @abstractmethod
    async def setup_group_id(self) -> None:
        pass

    @abstractmethod
    async def find_server_id(self) -> Optional[int]:
        pass

    @abstractmethod
    async def add_callback_server(self) -> Any:
        pass

    @abstractmethod
    async def delete_callback_server(self, server_id: int) -> Any:
        pass

    @abstractmethod
    async def edit_callback_server(self, server_id: int, secret_key: Optional[str] = None) -> Any:
        pass

    @abstractmethod
    async def get_callback_confirmation_code(self) -> Any:
        pass

    @abstractmethod
    async def get_callback_servers(self, server_ids: Optional[List[int]] = None) -> Any:
        pass

    @abstractmethod
    async def get_callback_settings(self, server_id: int) -> Any:
        pass

    @abstractmethod
    async def set_callback_settings(
        self, server_id: int, params: Optional[Dict[str, bool]] = None
    ) -> Any:
        pass

    @property
    @abstractmethod
    def api(self) -> "ABCAPI":
        pass

    @api.setter
    def api(self, new_api: "ABCAPI"):
        pass

    @abstractmethod
    def construct(
        self, api: "ABCAPI", error_handler: Optional["ABCErrorHandler"] = None
    ) -> "ABCCallback":
        pass
