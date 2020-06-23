import typing
from vkbottle.http import HTTPRequest
from vkbottle.utils import ContextInstanceMixin, Constructor, method_requested
from .error_handler.error_handler import VKErrorHandler

from pydantic import BaseModel
from .request import Request
from .category import Categories
from vkbottle.api.api.util.builtin import (
    AbstractTokenGenerator,
    ConsistentTokenGenerator,
    GENERATORS,
)

if typing.TYPE_CHECKING:
    from vkbottle.framework.framework.extensions.extension import AbstractExtension
    from vkbottle.types.methods.method import BaseMethod


class API(ContextInstanceMixin, Categories, Constructor):
    """ Main VK API object
    Possess user_id/group_id getters, request, constructor
    """

    def __init__(
        self,
        tokens: typing.Union[str, typing.List[str]] = None,
        generator: typing.Union[str] = "consistent",
        throw_errors: bool = True,
    ):
        if not isinstance(tokens, list):
            tokens = [tokens]

        self.token_generator: AbstractTokenGenerator = GENERATORS.get(
            generator, ConsistentTokenGenerator
        )(tokens)
        self._http: HTTPRequest = HTTPRequest()
        self.throw_errors: bool = throw_errors
        self._group_id: typing.Optional[int] = None
        self._user_id: typing.Optional[int] = None

        # Construct values
        self.error_handler: typing.Optional["VKErrorHandler"] = None
        self.extension: typing.Optional["AbstractExtension"] = None

        for category in self.__categories__:
            setattr(self, category, getattr(self, category)(self.api))

    def api(self, method: str, params: dict, **kwargs) -> typing.Awaitable:
        """ Return an awaitable request
        :param method: method's name to make a request and pass to the token_generator
        :param params: params dict is passed to the token_generator and used to make a request
        """
        for k, v in params.items():
            if isinstance(v, (tuple, list)):
                params[k] = ",".join(repr(i) for i in v)

        request = Request(self.token_generator, self.error_handler)
        return request(method, params, **kwargs)

    async def request(
        self,
        method: str,
        params: dict,
        throw_errors: typing.Optional[bool] = None,
        response_model: typing.Optional[BaseModel] = None,
        raw_response: bool = False,
    ) -> typing.Union[dict, BaseModel]:
        """Make a request"""
        return await self.api(
            method,
            params,
            throw_errors=throw_errors,
            response_model=response_model,
            raw_response=raw_response,
        )

    async def execute(self, code: str) -> typing.Any:
        """ Make an execute method """
        return await self.request("execute", {"code": code})

    @staticmethod
    def get_method_requested(method: str) -> "BaseMethod":
        return method_requested(method, Categories, None)

    def construct(
        self, error_handler: "VKErrorHandler", extension: "AbstractExtension"
    ) -> "API":
        self.error_handler = error_handler
        self.extension = extension
        return self

    @property
    async def user_id(self):
        if self._user_id is None:
            current_user = await self.users.get()
            self._user_id = current_user[0].id
        return self._user_id

    @property
    async def group_id(self):
        if self._group_id is None:
            current_user = await self.groups.get_by_id()
            self._group_id = current_user[0].id
        return self._group_id

    @group_id.setter
    def group_id(self, group_id: int):
        self._group_id = group_id

    @user_id.setter
    def user_id(self, user_id: int):
        self._user_id = user_id

    def __dict__(self):
        return {
            "generator": self.token_generator.__class__.__qualname__,
            "throw_errors": self.throw_errors,
            "tokens_amount": len(self.token_generator),
        }

    def __repr__(self):
        return f"<API {self.__dict__()} ({self._group_id or self._user_id})>"


class UserApi(API, ContextInstanceMixin):
    pass


class Api(API, ContextInstanceMixin):
    pass


def get_api() -> "API":
    return Api.get_current() or UserApi.get_current()
