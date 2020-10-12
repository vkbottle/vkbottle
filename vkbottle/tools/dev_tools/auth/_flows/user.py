from abc import ABC
from functools import reduce
from typing import Union, List, Optional
from vkbottle.http import AiohttpClient
from ..models import UserCodeFlowResponse
from pydantic.error_wrappers import ValidationError


class ABCUserAuthFlow(ABC):
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
    def _parse_scope(scope: Union[None, int, List[int]]) -> Union[None, int]:
        if isinstance(scope, List):
            return reduce(lambda a, b: a + b, scope)
        return scope


class UserImplicitFlow(ABCUserAuthFlow):
    """
    Implicit Flow Authorization class
    vk.com/dev/implicit_flow_user
    """

    def __init__(
            self,
            client_id: Union[int],
            redirect_uri: str,
            display: Optional[str] = None,
            scope: Union[None, int, List[int]] = None,
            state: Optional[str] = None,
            revoke: Optional[int] = None
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.display = display
        self.scope = self._parse_scope(scope)
        self.state = state
        self.revoke = revoke
        self.response_type = "token"


class UserAuthorizationCodeFlow(ABCUserAuthFlow):
    """
    Implicit Flow Authorization class
    vk.com/dev/authcode_flow_user
    """

    def __init__(
            self,
            client_id: Union[int],
            redirect_uri: str,
            display: Optional[str] = None,
            scope: Union[None, int, List[int]] = None,
            state: Optional[str] = None
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.display = display
        self.scope = self._parse_scope(scope)
        self.state = state
        self.response_type = "code"

    async def validate_code(self, client_secret: str, code: str) -> UserCodeFlowResponse:
        """Verify and return token, raise VKAuthError otherwise"""
        validation_link = f"{self._OAUTH_URL}access_token?" \
                          f"client_id={self.client_id}&" \
                          f"client_secret={client_secret}&" \
                          f"redirect_uri={self.redirect_uri}&" \
                          f"code={code}"
        http = AiohttpClient()
        response = await http.request_json("get", validation_link)
        await http.close()
        try:
            return UserCodeFlowResponse(**response)
        except ValidationError:
            raise Exception
            # TODO: raise VKAuthError
