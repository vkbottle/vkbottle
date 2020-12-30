from pydantic.error_wrappers import ValidationError

from vkbottle.exception_factory import VKAPIError
from vkbottle.http import AiohttpClient

from ..models import CredentialsFlowResponse, RequestTokenError


class ClientCredentialsFlow:
    """
    WARNING: this is an old flow, consider visiting vk.com/dev/service_token
    Documentation: vk.com/dev/client_cred_flow
    """

    def __init__(
        self, client_id: int, client_secret: str, v: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = "client_credentials"
        self.v = v

    @property
    def token_request_link(self) -> str:
        return (
            f"https://oauth.vk.com/access_token?"
            f"client_id={self.client_id}&"
            f"client_secret={self.client_secret}&"
            f"v={self.v}&"
            f"grant_type={self.grant_type}"
        )

    async def request_token(self, client_secret: str, code: str) -> CredentialsFlowResponse:
        """Request and return token, raise VKAuthError otherwise"""
        http = AiohttpClient()
        response = await http.request_json("get", self.token_request_link)
        await http.close()
        try:
            return CredentialsFlowResponse(**response)
        except ValidationError:
            error = RequestTokenError(**response)
            raise VKAPIError(error_description=str(error))
