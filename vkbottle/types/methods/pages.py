# Generated with love
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class PagesClearCache(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, url: str) -> responses.ok_response.OkResponse:
        """ pages.clearCache
        From Vk Docs: Allows to clear the cache of particular 'external' pages which may be attached to VK posts.
        Access from user, service token(s)
        :param url: Address of the page where you need to refesh the cached version
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.clearCache",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PagesGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int = None,
        page_id: int = None,
        global_: bool = None,
        site_preview: bool = None,
        title: str = None,
        need_source: bool = None,
        need_html: bool = None,
    ) -> responses.pages.Get:
        """ pages.get
        From Vk Docs: Returns information about a wiki page.
        Access from user token(s)
        :param owner_id: Page owner ID.
        :param page_id: Wiki page ID.
        :param global: '1' — to return information about a global wiki page
        :param site_preview: '1' — resulting wiki page is a preview for the attached link
        :param title: Wiki page title.
        :param need_source: 
        :param need_html: '1' — to return the page as HTML,
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.get", params, response_model=responses.pages.GetModel
        )


class PagesGetHistory(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, page_id: int, group_id: int = None, user_id: int = None
    ) -> responses.pages.GetHistory:
        """ pages.getHistory
        From Vk Docs: Returns a list of all previous versions of a wiki page.
        Access from user token(s)
        :param page_id: Wiki page ID.
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.getHistory", params, response_model=responses.pages.GetHistoryModel
        )


class PagesGetTitles(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int = None) -> responses.pages.GetTitles:
        """ pages.getTitles
        From Vk Docs: Returns a list of wiki pages in a group.
        Access from user token(s)
        :param group_id: ID of the community that owns the wiki page.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.getTitles", params, response_model=responses.pages.GetTitlesModel
        )


class PagesGetVersion(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        version_id: int,
        group_id: int = None,
        user_id: int = None,
        need_html: bool = None,
    ) -> responses.pages.GetVersion:
        """ pages.getVersion
        From Vk Docs: Returns the text of one of the previous versions of a wiki page.
        Access from user token(s)
        :param version_id: 
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: 
        :param need_html: '1' — to return the page as HTML
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.getVersion", params, response_model=responses.pages.GetVersionModel
        )


class PagesParseWiki(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, text: str, group_id: int = None
    ) -> responses.pages.ParseWiki:
        """ pages.parseWiki
        From Vk Docs: Returns HTML representation of the wiki markup.
        Access from user token(s)
        :param text: Text of the wiki page.
        :param group_id: ID of the group in the context of which this markup is interpreted.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.parseWiki", params, response_model=responses.pages.ParseWikiModel
        )


class PagesSave(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        text: str = None,
        page_id: int = None,
        group_id: int = None,
        user_id: int = None,
        title: str = None,
    ) -> responses.pages.Save:
        """ pages.save
        From Vk Docs: Saves the text of a wiki page.
        Access from user token(s)
        :param text: Text of the wiki page in wiki-format.
        :param page_id: Wiki page ID. The 'title' parameter can be passed instead of 'pid'.
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: User ID
        :param title: Wiki page title.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.save", params, response_model=responses.pages.SaveModel
        )


class PagesSaveAccess(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        page_id: int,
        group_id: int = None,
        user_id: int = None,
        view: int = None,
        edit: int = None,
    ) -> responses.pages.SaveAccess:
        """ pages.saveAccess
        From Vk Docs: Saves modified read and edit access settings for a wiki page.
        Access from user token(s)
        :param page_id: Wiki page ID.
        :param group_id: ID of the community that owns the wiki page.
        :param user_id: 
        :param view: Who can view the wiki page: '1' — only community members, '2' — all users can view the page, '0' — only community managers
        :param edit: Who can edit the wiki page: '1' — only community members, '2' — all users can edit the page, '0' — only community managers
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "pages.saveAccess", params, response_model=responses.pages.SaveAccessModel
        )


class Pages:
    def __init__(self, request):
        self.clear_cache = PagesClearCache(request)
        self.get = PagesGet(request)
        self.get_history = PagesGetHistory(request)
        self.get_titles = PagesGetTitles(request)
        self.get_version = PagesGetVersion(request)
        self.parse_wiki = PagesParseWiki(request)
        self.save = PagesSave(request)
        self.save_access = PagesSaveAccess(request)
