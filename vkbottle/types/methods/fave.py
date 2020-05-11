# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class FaveAddArticle(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, url: str) -> responses.ok_response.OkResponse:
        """ fave.addArticle
        From Vk Docs: 
        Access from user token(s)
        :param url: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addArticle",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveAddLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, link: str) -> responses.ok_response.OkResponse:
        """ fave.addLink
        From Vk Docs: Adds a link to user faves.
        Access from user token(s)
        :param link: Link URL.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addLink", params, response_model=responses.ok_response.OkResponseModel
        )


class FaveAddPage(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ fave.addPage
        From Vk Docs: 
        Access from user token(s)
        :param user_id: 
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addPage", params, response_model=responses.ok_response.OkResponseModel
        )


class FaveAddPost(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, id: int, access_key: str = None
    ) -> responses.ok_response.OkResponse:
        """ fave.addPost
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param id: 
        :param access_key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addPost", params, response_model=responses.ok_response.OkResponseModel
        )


class FaveAddProduct(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, id: int, access_key: str = None
    ) -> responses.ok_response.OkResponse:
        """ fave.addProduct
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param id: 
        :param access_key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addProduct",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveAddTag(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, name: str = None) -> responses.fave.AddTag:
        """ fave.addTag
        From Vk Docs: 
        Access from user token(s)
        :param name: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addTag", params, response_model=responses.fave.AddTagModel
        )


class FaveAddVideo(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, id: int, access_key: str = None
    ) -> responses.ok_response.OkResponse:
        """ fave.addVideo
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param id: 
        :param access_key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.addVideo",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveEditTag(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, id: int, name: str) -> responses.ok_response.OkResponse:
        """ fave.editTag
        From Vk Docs: 
        Access from user token(s)
        :param id: 
        :param name: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.editTag", params, response_model=responses.ok_response.OkResponseModel
        )


class FaveGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        extended: bool = None,
        item_type: str = None,
        tag_id: int = None,
        offset: int = None,
        count: int = None,
        fields: str = None,
        is_from_snackbar: bool = None,
    ) -> responses.fave.Get:
        """ fave.get
        From Vk Docs: 
        Access from user token(s)
        :param extended: '1' — to return additional 'wall', 'profiles', and 'groups' fields. By default: '0'.
        :param item_type: 
        :param tag_id: Tag ID.
        :param offset: Offset needed to return a specific subset of users.
        :param count: Number of users to return.
        :param fields: 
        :param is_from_snackbar: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.get", params, response_model=responses.fave.GetModel
        )


class FaveGetPages(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        offset: int = None,
        count: int = None,
        type: str = None,
        fields: typing.List = None,
        tag_id: int = None,
    ) -> responses.fave.GetPages:
        """ fave.getPages
        From Vk Docs: 
        Access from user token(s)
        :param offset: 
        :param count: 
        :param type: 
        :param fields: 
        :param tag_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.getPages", params, response_model=responses.fave.GetPagesModel
        )


class FaveGetTags(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> responses.fave.GetTags:
        """ fave.getTags
        From Vk Docs: 
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.getTags", params, response_model=responses.fave.GetTagsModel
        )


class FaveMarkSeen(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> responses.ok_response.OkResponse:
        """ fave.markSeen
        From Vk Docs: 
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.markSeen",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveRemoveArticle(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, article_id: int
    ) -> responses.ok_response.OkResponse:
        """ fave.removeArticle
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param article_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.removeArticle",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveRemoveLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, link_id: str = None, link: str = None
    ) -> responses.ok_response.OkResponse:
        """ fave.removeLink
        From Vk Docs: Removes link from the user's faves.
        Access from user token(s)
        :param link_id: Link ID (can be obtained by [vk.com/dev/faves.getLinks|faves.getLinks] method).
        :param link: Link URL
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.removeLink",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveRemovePage(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ fave.removePage
        From Vk Docs: 
        Access from user token(s)
        :param user_id: 
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.removePage",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveRemovePost(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, id: int
    ) -> responses.ok_response.OkResponse:
        """ fave.removePost
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.removePost",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveRemoveProduct(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, id: int
    ) -> responses.ok_response.OkResponse:
        """ fave.removeProduct
        From Vk Docs: 
        Access from user token(s)
        :param owner_id: 
        :param id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.removeProduct",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveRemoveTag(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, id: int) -> responses.ok_response.OkResponse:
        """ fave.removeTag
        From Vk Docs: 
        Access from user token(s)
        :param id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.removeTag",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveReorderTags(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, ids: typing.List) -> responses.ok_response.OkResponse:
        """ fave.reorderTags
        From Vk Docs: 
        Access from user token(s)
        :param ids: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.reorderTags",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveSetPageTags(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, group_id: int = None, tag_ids: typing.List = None
    ) -> responses.ok_response.OkResponse:
        """ fave.setPageTags
        From Vk Docs: 
        Access from user token(s)
        :param user_id: 
        :param group_id: 
        :param tag_ids: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.setPageTags",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FaveSetTags(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        item_type: str = None,
        item_owner_id: int = None,
        item_id: int = None,
        tag_ids: typing.List = None,
        link_id: str = None,
        link_url: str = None,
    ) -> responses.ok_response.OkResponse:
        """ fave.setTags
        From Vk Docs: 
        Access from user token(s)
        :param item_type: 
        :param item_owner_id: 
        :param item_id: 
        :param tag_ids: 
        :param link_id: 
        :param link_url: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.setTags", params, response_model=responses.ok_response.OkResponseModel
        )


class FaveTrackPageInteraction(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ fave.trackPageInteraction
        From Vk Docs: 
        Access from user token(s)
        :param user_id: 
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "fave.trackPageInteraction",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Fave:
    def __init__(self, request):
        self.add_article = FaveAddArticle(request)
        self.add_link = FaveAddLink(request)
        self.add_page = FaveAddPage(request)
        self.add_post = FaveAddPost(request)
        self.add_product = FaveAddProduct(request)
        self.add_tag = FaveAddTag(request)
        self.add_video = FaveAddVideo(request)
        self.edit_tag = FaveEditTag(request)
        self.get = FaveGet(request)
        self.get_pages = FaveGetPages(request)
        self.get_tags = FaveGetTags(request)
        self.mark_seen = FaveMarkSeen(request)
        self.remove_article = FaveRemoveArticle(request)
        self.remove_link = FaveRemoveLink(request)
        self.remove_page = FaveRemovePage(request)
        self.remove_post = FaveRemovePost(request)
        self.remove_product = FaveRemoveProduct(request)
        self.remove_tag = FaveRemoveTag(request)
        self.reorder_tags = FaveReorderTags(request)
        self.set_page_tags = FaveSetPageTags(request)
        self.set_tags = FaveSetTags(request)
        self.track_page_interaction = FaveTrackPageInteraction(request)
