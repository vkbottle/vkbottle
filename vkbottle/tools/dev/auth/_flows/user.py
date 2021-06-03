from typing import List, Optional, Union

from ..models import UserCodeFlowResponse
from .abc import ABCAuthorizationCodeFlow, ABCImplicitFlow


class UserImplicitFlow(ABCImplicitFlow):
    """
    User Implicit Flow class
    Documentation: vk.com/dev/implicit_flow_user
    """

    def __init__(
        self,
        client_id: Union[int],
        redirect_uri: str,
        display: Optional[str] = None,
        scope: Optional[Union[int, List[int]]] = None,
        state: Optional[str] = None,
        revoke: Optional[int] = None,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.display = display
        self.scope = self.parse_scope(scope)
        self.response_type = "token"
        self.state = state
        self.revoke = revoke


class UserAuthorizationCodeFlow(ABCAuthorizationCodeFlow):
    """
    User Authorization Code Flow class
    Documentation: vk.com/dev/authcode_flow_user
    """

    def __init__(
        self,
        client_id: Union[int],
        redirect_uri: str,
        display: Optional[str] = None,
        scope: Optional[Union[int, List[int]]] = None,
        state: Optional[str] = None,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.display = display
        self.scope = self.parse_scope(scope)
        self.response_type = "code"
        self.state = state

    @staticmethod
    def get_model():
        return UserCodeFlowResponse

    def get_token_request_link(self, client_secret, code):
        return (
            f"{self._OAUTH_URL}access_token?"
            f"client_id={self.client_id}&"
            f"client_secret={client_secret}&"
            f"redirect_uri={self.redirect_uri}&"
            f"code={code}"
        )
