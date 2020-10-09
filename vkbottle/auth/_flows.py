from typing import Union, List
from functools import reduce


class AuthFlow:
    _OAUTH_URL = "https://oauth.vk.com/"

    def __init__(
            self,
            client_id: Union[int],
            redirect_uri: str,
            display: Union[None, str] = None,
            scope: Union[None, int] = None,
            response_type: Union[None, str] = None,
            state: Union[None, str] = None,
            revoke: Union[None, int] = None
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.display = display
        self.scope = scope
        self.response_type = response_type
        self.state = state
        self.revoke = revoke

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


class ImplicitFlow(AuthFlow):
    def __init__(
            self,
            client_id: int,
            redirect_uri: str,
            display: Union[None, str] = None,
            scope: Union[None, int, List[int]] = None,
            state: Union[None, str] = None,
            revoke: int = 1
    ):
        super().__init__(
            client_id=client_id,
            redirect_uri=redirect_uri,
            display=display,
            scope=self._parse_scope(scope),
            response_type="token",
            state=state,
            revoke=revoke
        )


class AuthorizationCodeFlow(AuthFlow):
    def __init__(
            self,
            client_id: int,
            redirect_uri: str,
            display: Union[None, str] = None,
            scope: Union[None, int, List[int]] = None,
            state: Union[None, str] = None
    ):
        super().__init__(
            client_id=client_id,
            redirect_uri=redirect_uri,
            display=display,
            scope=self._parse_scope(scope),
            response_type="code",
            state=state
        )

    def validate_code(self, client_secret: str, code: str) -> str:
        """Verify and return token, raise VKAuthError otherwise"""
        validation_link = f"{self._OAUTH_URL}access_token?" \
                          f"client_id={self.client_id}&" \
                          f"client_secret={client_secret}&" \
                          f"redirect_uri={self.redirect_uri}&" \
                          f"code={code}"
        # TODO: Validation request
        # TODO: Add VKAuthError factory
        return ""
