from abc import ABC, abstractmethod
from functools import reduce
from typing import List, Optional, Union

from pydantic.error_wrappers import ValidationError

from vkbottle.exception_factory import VKAPIError
from vkbottle.http import AiohttpClient

from ..models import RequestTokenError, UserCodeFlowResponse


class ABCAuthFlow(ABC):
    """Abstract auth flow class"""

    _OAUTH_URL = "https://oauth.vk.com/"

    @property
    def auth_dialog_link(self) -> str:
        """Get auth link"""
        link = f"{self._OAUTH_URL}authorize?"
        for key, value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                link += f"{key}={value}&"
        return link

    @staticmethod
    def parse_scope(scope: Optional[Union[int, List[int]]]) -> Optional[int]:
        if isinstance(scope, List):
            return reduce(lambda a, b: a + b, scope)
        return scope


class ABCImplicitFlow(ABCAuthFlow):
    pass


class ABCAuthorizationCodeFlow(ABCAuthFlow):
    @staticmethod
    @abstractmethod
    def get_model():
        """Validation response model"""

    @abstractmethod
    def get_token_request_link(self, client_secret: str, code: str) -> str:
        pass

    async def request_token(self, client_secret: str, code: str) -> UserCodeFlowResponse:
        """Request and return token, raise VKAuthError otherwise"""
        http = AiohttpClient()
        response = await http.request_json("get", self.get_token_request_link(client_secret, code))
        await http.close()
        try:
            return self.get_model()(**response)
        except ValidationError:
            error = RequestTokenError(**response)
            raise VKAPIError(error_description=str(error))
