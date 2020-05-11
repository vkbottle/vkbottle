# Generated with love
import typing
from .access import APIAccessibility
from .method import BaseMethod


class PrettycardsCreate(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        title: str,
        photo: str,
        link: str,
        price: str = None,
        price_old: str = None,
        button: str = None,
    ) -> dict:
        """ prettyCards.create
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param photo: 
        :param title: 
        :param link: 
        :param price: 
        :param price_old: 
        :param button: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("prettyCards.create", params)


class PrettycardsDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, card_id: int) -> dict:
        """ prettyCards.delete
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param card_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("prettyCards.delete", params)


class PrettycardsEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        card_id: int,
        photo: str = None,
        title: str = None,
        link: str = None,
        price: str = None,
        price_old: str = None,
        button: str = None,
    ) -> dict:
        """ prettyCards.edit
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param card_id: 
        :param photo: 
        :param title: 
        :param link: 
        :param price: 
        :param price_old: 
        :param button: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("prettyCards.edit", params)


class PrettycardsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, offset: int = None, count: int = None
    ) -> dict:
        """ prettyCards.get
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param offset: 
        :param count: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("prettyCards.get", params)


class PrettycardsGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, card_ids: typing.List) -> dict:
        """ prettyCards.getById
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param card_ids: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("prettyCards.getById", params)


class PrettycardsGetUploadURL(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> dict:
        """ prettyCards.getUploadURL
        From Vk Docs: 
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request("prettyCards.getUploadURL", params)


class Prettycards:
    def __init__(self, request):
        self.create = PrettycardsCreate(request)
        self.delete = PrettycardsDelete(request)
        self.edit = PrettycardsEdit(request)
        self.get = PrettycardsGet(request)
        self.get_by_id = PrettycardsGetById(request)
        self.get_upload_u_r_l = PrettycardsGetUploadURL(request)
