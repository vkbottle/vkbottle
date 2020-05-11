# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class DocsAdd(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, doc_id: int, access_key: str = None
    ) -> responses.docs.Add:
        """ docs.add
        From Vk Docs: Copies a document to a user's or community's document list.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the document. Use a negative value to designate a community ID.
        :param doc_id: Document ID.
        :param access_key: Access key. This parameter is required if 'access_key' was returned with the document's data.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.add", params, response_model=responses.docs.AddModel
        )


class DocsDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, doc_id: int
    ) -> responses.ok_response.OkResponse:
        """ docs.delete
        From Vk Docs: Deletes a user or community document.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the document. Use a negative value to designate a community ID.
        :param doc_id: Document ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.delete", params, response_model=responses.ok_response.OkResponseModel
        )


class DocsEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, doc_id: int, title: str = None, tags: typing.List = None
    ) -> responses.ok_response.OkResponse:
        """ docs.edit
        From Vk Docs: Edits a document.
        Access from user token(s)
        :param owner_id: User ID or community ID. Use a negative value to designate a community ID.
        :param doc_id: Document ID.
        :param title: Document title.
        :param tags: Document tags.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.edit", params, response_model=responses.ok_response.OkResponseModel
        )


class DocsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        count: int = None,
        offset: int = None,
        type: int = None,
        owner_id: int = None,
    ) -> responses.docs.Get:
        """ docs.get
        From Vk Docs: Returns detailed information about user or community documents.
        Access from user token(s)
        :param count: Number of documents to return. By default, all documents.
        :param offset: Offset needed to return a specific subset of documents.
        :param type: 
        :param owner_id: ID of the user or community that owns the documents. Use a negative value to designate a community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.get", params, response_model=responses.docs.GetModel
        )


class DocsGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, docs: typing.List) -> responses.docs.GetById:
        """ docs.getById
        From Vk Docs: Returns information about documents by their IDs.
        Access from user token(s)
        :param docs: Document IDs. Example: , "66748_91488,66748_91455",
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.getById", params, response_model=responses.docs.GetByIdModel
        )


class DocsGetMessagesUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, type: str = None, peer_id: int = None
    ) -> responses.base.GetUploadServer:
        """ docs.getMessagesUploadServer
        From Vk Docs: Returns the server address for document upload.
        Access from user, group token(s)
        :param type: Document type.
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'Chat ID', e.g. '2000000001'. For community: '- Community ID', e.g. '-12345'. "
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.getMessagesUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class DocsGetTypes(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int) -> responses.docs.GetTypes:
        """ docs.getTypes
        From Vk Docs: Returns documents types available for current user.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the documents. Use a negative value to designate a community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.getTypes", params, response_model=responses.docs.GetTypesModel
        )


class DocsGetUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int = None) -> responses.base.GetUploadServer:
        """ docs.getUploadServer
        From Vk Docs: Returns the server address for document upload.
        Access from user token(s)
        :param group_id: Community ID (if the document will be uploaded to the community).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.getUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class DocsGetWallUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, group_id: int = None) -> responses.base.GetUploadServer:
        """ docs.getWallUploadServer
        From Vk Docs: Returns the server address for document upload onto a user's or community's wall.
        Access from user, group token(s)
        :param group_id: Community ID (if the document will be uploaded to the community).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.getWallUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class DocsSave(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, file: str, title: str = None, tags: str = None
    ) -> responses.docs.Save:
        """ docs.save
        From Vk Docs: Saves a document after [vk.com/dev/upload_files_2|uploading it to a server].
        Access from user, group token(s)
        :param file: This parameter is returned when the file is [vk.com/dev/upload_files_2|uploaded to the server].
        :param title: Document title.
        :param tags: Document tags.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.save", params, response_model=responses.docs.SaveModel
        )


class DocsSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, q: str, search_own: bool = None, count: int = None, offset: int = None
    ) -> responses.docs.Search:
        """ docs.search
        From Vk Docs: Returns a list of documents matching the search criteria.
        Access from user, group token(s)
        :param q: Search query string.
        :param search_own: 
        :param count: Number of results to return.
        :param offset: Offset needed to return a specific subset of results.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "docs.search", params, response_model=responses.docs.SearchModel
        )


class Docs:
    def __init__(self, request):
        self.add = DocsAdd(request)
        self.delete = DocsDelete(request)
        self.edit = DocsEdit(request)
        self.get = DocsGet(request)
        self.get_by_id = DocsGetById(request)
        self.get_messages_upload_server = DocsGetMessagesUploadServer(request)
        self.get_types = DocsGetTypes(request)
        self.get_upload_server = DocsGetUploadServer(request)
        self.get_wall_upload_server = DocsGetWallUploadServer(request)
        self.save = DocsSave(request)
        self.search = DocsSearch(request)
