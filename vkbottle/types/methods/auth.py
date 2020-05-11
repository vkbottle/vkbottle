# Generated with love
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class AuthCheckPhone(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER, APIAccessibility.OPEN]

    async def __call__(
        self,
        phone: str,
        client_id: int = None,
        client_secret: str = None,
        auth_by_phone: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ auth.checkPhone
        From Vk Docs: Checks a user's phone number for correctness.
        Access from user, open token(s)
        :param phone: Phone number.
        :param client_id: User ID.
        :param client_secret: 
        :param auth_by_phone: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "auth.checkPhone",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class AuthRestore(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER, APIAccessibility.OPEN]

    async def __call__(self, phone: str, last_name: str) -> responses.auth.Restore:
        """ auth.restore
        From Vk Docs: Allows to restore account access using a code received via SMS. " This method is only available for apps with [vk.com/dev/auth_direct|Direct authorization] access. "
        Access from user, open token(s)
        :param phone: User phone number.
        :param last_name: User last name.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "auth.restore", params, response_model=responses.auth.RestoreModel
        )


class Auth:
    def __init__(self, request):
        self.check_phone = AuthCheckPhone(request)
        self.restore = AuthRestore(request)
