# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class NotesAdd(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        title: str,
        text: str,
        privacy_view: typing.List,
        privacy_comment: typing.List,
    ):
        """ notes.add
        From Vk Docs: Creates a new note for the current user.
        Access from user token(s)
        :param title: Note title.
        :param text: Note text.
        :param privacy_view: 
        :param privacy_comment: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.add", params)


class NotesCreateComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, note_id: int, owner_id: int, reply_to: int, message: str, guid: str
    ):
        """ notes.createComment
        From Vk Docs: Adds a new comment on a note.
        Access from user token(s)
        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param reply_to: ID of the user to whom the reply is addressed (if the comment is a reply to another comment).
        :param message: Comment text.
        :param guid: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.createComment", params)


class NotesDelete(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, note_id: int):
        """ notes.delete
        From Vk Docs: Deletes a note of the current user.
        Access from user token(s)
        :param note_id: Note ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.delete", params)


class NotesDeleteComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, comment_id: int, owner_id: int):
        """ notes.deleteComment
        From Vk Docs: Deletes a comment on a note.
        Access from user token(s)
        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.deleteComment", params)


class NotesEdit(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        note_id: int,
        title: str,
        text: str,
        privacy_view: typing.List,
        privacy_comment: typing.List,
    ):
        """ notes.edit
        From Vk Docs: Edits a note of the current user.
        Access from user token(s)
        :param note_id: Note ID.
        :param title: Note title.
        :param text: Note text.
        :param privacy_view: 
        :param privacy_comment: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.edit", params)


class NotesEditComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, comment_id: int, owner_id: int, message: str):
        """ notes.editComment
        From Vk Docs: Edits a comment on a note.
        Access from user token(s)
        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        :param message: New comment text.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.editComment", params)


class NotesGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, note_ids: typing.List, user_id: int, offset: int, count: int, sort: int
    ):
        """ notes.get
        From Vk Docs: Returns a list of notes created by a user.
        Access from user token(s)
        :param note_ids: Note IDs.
        :param user_id: Note owner ID.
        :param offset: 
        :param count: Number of notes to return.
        :param sort: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.get", params)


class NotesGetById(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, note_id: int, owner_id: int, need_wiki: bool):
        """ notes.getById
        From Vk Docs: Returns a note by its ID.
        Access from user token(s)
        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param need_wiki: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.getById", params)


class NotesGetComments(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, note_id: int, owner_id: int, sort: int, offset: int, count: int
    ):
        """ notes.getComments
        From Vk Docs: Returns a list of comments on a note.
        Access from user token(s)
        :param note_id: Note ID.
        :param owner_id: Note owner ID.
        :param sort: 
        :param offset: 
        :param count: Number of comments to return.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.getComments", params)


class NotesRestoreComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, comment_id: int, owner_id: int):
        """ notes.restoreComment
        From Vk Docs: Restores a deleted comment on a note.
        Access from user token(s)
        :param comment_id: Comment ID.
        :param owner_id: Note owner ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("notes.restoreComment", params)


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
