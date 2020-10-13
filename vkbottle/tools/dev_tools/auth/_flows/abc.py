from abc import ABC
from abc import abstractmethod
from functools import reduce
from typing import Union, List, Optional

from pydantic.error_wrappers import ValidationError

from vkbottle.http import AiohttpClient
from ..models import UserCodeFlowResponse


class ABCAuthFlow(ABC):
    """Abstract auth flow class"""
    _OAUTH_URL = "https://oauth.vk.com/"

    @property
    def auth_dialog_link(self) -> str:
        """Get auth link"""
        link = f"{self._OAUTH_URL}authorize?"
        for key, value in self.__dict__.items():
            if not key.startswith('_') and value is not None:
                link += f"{key}={value}&"
        return link

    @staticmethod
    def parse_scope(scope: Optional[Union[int, List[int]]]) -> Optional[int]:
        if isinstance(scope, List):
            return reduce(lambda a, b: a + b, scope)
        return scope


class ABCImplicitFlow(ABCAuthFlow):
    pass


class ABCAuthCodeFlow(ABCAuthFlow):

    @staticmethod
    @abstractmethod
    def get_model():
        """Validation response model"""
        pass

    @abstractmethod
    def get_validation_link(self, client_secret: str, code: str) -> str:
        pass

    async def validate_code(self, client_secret: str, code: str) -> UserCodeFlowResponse:
        """Verify and return token, raise VKAuthError otherwise"""
        http = AiohttpClient()
        response = await http.request_json("get", self.get_validation_link(client_secret, code))
        await http.close()
        try:
            return self.get_model()(**response)
        except ValidationError:
            raise Exception
            # TODO: raise VKAuthError
