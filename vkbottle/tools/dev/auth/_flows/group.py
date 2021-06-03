from typing import List, Optional, Union

from ..models import GroupCodeFlowResponse
from .abc import ABCAuthorizationCodeFlow, ABCImplicitFlow


class GroupImplicitFlow(ABCImplicitFlow):
    """
    Group Implicit Flow class
    Documentation: vk.com/dev/implicit_flow_group
    """

    def __init__(
        self,
        client_id: int,
        redirect_uri: str,
        v: str,
        display: Optional[str] = None,
        scope: Optional[Union[int, List[int]]] = None,
        state: Optional[str] = None,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.display = display
        self.scope = self.parse_scope(scope)
        self.state = state
        self.v = v
        self.response_type = "token"


class GroupAuthorizationCodeFlow(ABCAuthorizationCodeFlow):
    """
    Group Authorization Code Flow class
    Documentation: vk.com/dev/authcode_flow_group
    """

    def __init__(
        self,
        client_id: int,
        redirect_uri: str,
        group_ids: Union[str, List[Union[int, str]]],
        v: str,
        display: Optional[str] = None,
        scope: Optional[Union[int, List[int]]] = None,
        state: Optional[str] = None,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.group_ids = self.parse_group_ids(group_ids)
        self.display = display
        self.scope = self.parse_scope(scope)
        self.response_type = "code"
        self.v = v
        self.state = state

    @staticmethod
    def parse_group_ids(group_ids: Union[str, List[Union[int, str]]]) -> str:
        if isinstance(group_ids, List):
            return ",".join(map(lambda x: str(x), group_ids))
        return group_ids

    @staticmethod
    def get_model():
        return GroupCodeFlowResponse

    def get_token_request_link(self, client_secret, code):
        return (
            f"{self._OAUTH_URL}access_token?"
            f"client_id={self.client_id}&"
            f"client_secret={client_secret}&"
            f"redirect_uri={self.redirect_uri}&"
            f"code={code}"
        )
