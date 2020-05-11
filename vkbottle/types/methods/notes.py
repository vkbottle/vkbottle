# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class NotesAdd(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        title: str,
        text: str,
        privacy_view: typing.List = None,
        privacy_comment: typing.List = None,
    ) -> responses.notes.Add:
        """ notes.add
        From Vk Docs: Creates a new note for the current user.
        Access from user token(s)
        :param title: Note title.
        :param text: Note text.
        :param privacy_view: 
        :param privacy_comment: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.add", params, response_model=responses.notes.AddModel
        )


class NotesCreateComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        note_id: int,
        message: str,
        owner_id: int = None,
        reply_to: int = None,
        guid: str = None,
    ) -> responses.notes.CreateComment:
        """ notes.createComment
        From Vk Docs: Adds a new comment on a note.
        Access from user token(s)
        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param reply_to: ID of the user to whom the reply is addressed (if the comment is a reply to another comment).
        :param message: Comment text.
        :param guid: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.createComment",
            params,
            response_model=responses.notes.CreateCommentModel,
        )


class NotesDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, note_id: int) -> responses.ok_response.OkResponse:
        """ notes.delete
        From Vk Docs: Deletes a note of the current user.
        Access from user token(s)
        :param note_id: Note ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.delete", params, response_model=responses.ok_response.OkResponseModel
        )


class NotesDeleteComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ notes.deleteComment
        From Vk Docs: Deletes a comment on a note.
        Access from user token(s)
        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.deleteComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class NotesEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        note_id: int,
        text: str,
        title: str,
        privacy_view: typing.List = None,
        privacy_comment: typing.List = None,
    ) -> responses.ok_response.OkResponse:
        """ notes.edit
        From Vk Docs: Edits a note of the current user.
        Access from user token(s)
        :param note_id: Note ID.
        :param title: Note title.
        :param text: Note text.
        :param privacy_view: 
        :param privacy_comment: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.edit", params, response_model=responses.ok_response.OkResponseModel
        )


class NotesEditComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, message: str, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ notes.editComment
        From Vk Docs: Edits a comment on a note.
        Access from user token(s)
        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        :param message: New comment text.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.editComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class NotesGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        note_ids: typing.List = None,
        user_id: int = None,
        offset: int = None,
        count: int = None,
        sort: int = None,
    ) -> responses.notes.Get:
        """ notes.get
        From Vk Docs: Returns a list of notes created by a user.
        Access from user token(s)
        :param note_ids: Note IDs.
        :param user_id: Note owner ID.
        :param offset: 
        :param count: Number of notes to return.
        :param sort: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.get", params, response_model=responses.notes.GetModel
        )


class NotesGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, note_id: int, owner_id: int = None, need_wiki: bool = None
    ) -> responses.notes.GetById:
        """ notes.getById
        From Vk Docs: Returns a note by its ID.
        Access from user token(s)
        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param need_wiki: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.getById", params, response_model=responses.notes.GetByIdModel
        )


class NotesGetComments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        note_id: int,
        owner_id: int = None,
        sort: int = None,
        offset: int = None,
        count: int = None,
    ) -> responses.notes.GetComments:
        """ notes.getComments
        From Vk Docs: Returns a list of comments on a note.
        Access from user token(s)
        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param sort: 
        :param offset: 
        :param count: Number of comments to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.getComments", params, response_model=responses.notes.GetCommentsModel
        )


class NotesRestoreComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ notes.restoreComment
        From Vk Docs: Restores a deleted comment on a note.
        Access from user token(s)
        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notes.restoreComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Notes:
    def __init__(self, request):
        self.add = NotesAdd(request)
        self.create_comment = NotesCreateComment(request)
        self.delete = NotesDelete(request)
        self.delete_comment = NotesDeleteComment(request)
        self.edit = NotesEdit(request)
        self.edit_comment = NotesEditComment(request)
        self.get = NotesGet(request)
        self.get_by_id = NotesGetById(request)
        self.get_comments = NotesGetComments(request)
        self.restore_comment = NotesRestoreComment(request)
