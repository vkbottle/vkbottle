# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class MarketAdd(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        name: str,
        description: str,
        category_id: int,
        price: typing.Any,
        old_price: typing.Any,
        deleted: bool,
        main_photo_id: int,
        photo_ids: typing.List,
        url: str,
    ) -> responses.market.Add:
        """ market.add
        From Vk Docs: Ads a new item to the market.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param name: Item name.
        :param description: Item description.
        :param category_id: Item category ID.
        :param price: Item price.
        :param old_price: 
        :param deleted: Item status ('1' — deleted, '0' — not deleted).
        :param main_photo_id: Cover photo ID.
        :param photo_ids: IDs of additional photos.
        :param url: Url for button in market item.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.add", params, response_model=responses.market.Add
        )


class MarketAddAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, title: str, photo_id: int, main_album: bool
    ) -> responses.market.AddAlbum:
        """ market.addAlbum
        From Vk Docs: Creates new collection of items
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param title: Collection title.
        :param photo_id: Cover photo ID.
        :param main_album: Set as main ('1' – set, '0' – no).
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.addAlbum", params, response_model=responses.market.AddAlbum
        )


class MarketAddToAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, item_id: int, album_ids: typing.List
    ) -> responses.market.AddToAlbum:
        """ market.addToAlbum
        From Vk Docs: Adds an item to one or multiple collections.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param album_ids: Collections IDs to add item to.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.addToAlbum", params, response_model=responses.market.AddToAlbum
        )


class MarketCreateComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        item_id: int,
        message: str,
        attachments: typing.List,
        from_group: bool,
        reply_to_comment: int,
        sticker_id: int,
        guid: str,
    ) -> responses.market.CreateComment:
        """ market.createComment
        From Vk Docs: Creates a new comment for an item.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param message: Comment text (required if 'attachments' parameter is not specified)
        :param attachments: Comma-separated list of objects attached to a comment. The field is submitted the following way: , "'<owner_id>_<media_id>,<owner_id>_<media_id>'", , '' - media attachment type: "'photo' - photo, 'video' - video, 'audio' - audio, 'doc' - document", , '<owner_id>' - media owner id, '<media_id>' - media attachment id, , For example: "photo100172_166443618,photo66748_265827614",
        :param from_group: '1' - comment will be published on behalf of a community, '0' - on behalf of a user (by default).
        :param reply_to_comment: ID of a comment to reply with current comment to.
        :param sticker_id: Sticker ID.
        :param guid: Random value to avoid resending one comment.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.createComment",
            params,
            response_model=responses.market.CreateComment,
        )


class MarketDelete(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, item_id: int) -> responses.market.Delete:
        """ market.delete
        From Vk Docs: Deletes an item.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.delete", params, response_model=responses.market.Delete
        )


class MarketDeleteAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, album_id: int
    ) -> responses.market.DeleteAlbum:
        """ market.deleteAlbum
        From Vk Docs: Deletes a collection of items.
        Access from user token(s)
        :param owner_id: ID of an collection owner community.
        :param album_id: Collection ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.deleteAlbum", params, response_model=responses.market.DeleteAlbum
        )


class MarketDeleteComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int
    ) -> responses.market.DeleteComment:
        """ market.deleteComment
        From Vk Docs: Deletes an item's comment
        Access from user token(s)
        :param owner_id: identifier of an item owner community, "Note that community id in the 'owner_id' parameter should be negative number. For example 'owner_id'=-1 matches the [vk.com/apiclub|VK API] community "
        :param comment_id: comment id
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.deleteComment",
            params,
            response_model=responses.market.DeleteComment,
        )


class MarketEdit(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        item_id: int,
        name: str,
        description: str,
        category_id: int,
        price: typing.Any,
        deleted: bool,
        main_photo_id: int,
        photo_ids: typing.List,
        url: str,
    ) -> responses.market.Edit:
        """ market.edit
        From Vk Docs: Edits an item.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param name: Item name.
        :param description: Item description.
        :param category_id: Item category ID.
        :param price: Item price.
        :param deleted: Item status ('1' — deleted, '0' — not deleted).
        :param main_photo_id: Cover photo ID.
        :param photo_ids: IDs of additional photos.
        :param url: Url for button in market item.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.edit", params, response_model=responses.market.Edit
        )


class MarketEditAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, album_id: int, title: str, photo_id: int, main_album: bool
    ) -> responses.market.EditAlbum:
        """ market.editAlbum
        From Vk Docs: Edits a collection of items
        Access from user token(s)
        :param owner_id: ID of an collection owner community.
        :param album_id: Collection ID.
        :param title: Collection title.
        :param photo_id: Cover photo id
        :param main_album: Set as main ('1' – set, '0' – no).
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.editAlbum", params, response_model=responses.market.EditAlbum
        )


class MarketEditComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int, message: str, attachments: typing.List
    ) -> responses.market.EditComment:
        """ market.editComment
        From Vk Docs: Chages item comment's text
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param comment_id: Comment ID.
        :param message: New comment text (required if 'attachments' are not specified), , 2048 symbols maximum.
        :param attachments: Comma-separated list of objects attached to a comment. The field is submitted the following way: , "'<owner_id>_<media_id>,<owner_id>_<media_id>'", , '' - media attachment type: "'photo' - photo, 'video' - video, 'audio' - audio, 'doc' - document", , '<owner_id>' - media owner id, '<media_id>' - media attachment id, , For example: "photo100172_166443618,photo66748_265827614",
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.editComment", params, response_model=responses.market.EditComment
        )


class MarketGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, album_id: int, count: int, offset: int, extended: bool
    ) -> responses.market.Get:
        """ market.get
        From Vk Docs: Returns items list for a community.
        Access from user token(s)
        :param owner_id: ID of an item owner community, "Note that community id in the 'owner_id' parameter should be negative number. For example 'owner_id'=-1 matches the [vk.com/apiclub|VK API] community "
        :param album_id: 
        :param count: Number of items to return.
        :param offset: Offset needed to return a specific subset of results.
        :param extended: '1' – method will return additional fields: 'likes, can_comment, car_repost, photos'. These parameters are not returned by default.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.get", params, response_model=responses.market.Get
        )


class MarketGetAlbumById(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, album_ids: typing.List
    ) -> responses.market.GetAlbumById:
        """ market.getAlbumById
        From Vk Docs: Returns items album's data
        Access from user token(s)
        :param owner_id: identifier of an album owner community, "Note that community id in the 'owner_id' parameter should be negative number. For example 'owner_id'=-1 matches the [vk.com/apiclub|VK API] community "
        :param album_ids: collections identifiers to obtain data from
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.getAlbumById", params, response_model=responses.market.GetAlbumById
        )


class MarketGetAlbums(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, offset: int, count: int
    ) -> responses.market.GetAlbums:
        """ market.getAlbums
        From Vk Docs: Returns community's collections list.
        Access from user token(s)
        :param owner_id: ID of an items owner community.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of items to return.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.getAlbums", params, response_model=responses.market.GetAlbums
        )


class MarketGetById(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, item_ids: typing.List, extended: bool
    ) -> responses.market.GetById:
        """ market.getById
        From Vk Docs: Returns information about market items by their ids.
        Access from user token(s)
        :param item_ids: Comma-separated ids list: {user id}_{item id}. If an item belongs to a community -{community id} is used. " 'Videos' value example: , '-4363_136089719,13245770_137352259'"
        :param extended: '1' – to return additional fields: 'likes, can_comment, car_repost, photos'. By default: '0'.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.getById", params, response_model=responses.market.GetById
        )


class MarketGetCategories(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, count: int, offset: int
    ) -> responses.market.GetCategoriesResponse:
        """ market.getCategories
        From Vk Docs: Returns a list of market categories.
        Access from user token(s)
        :param count: Number of results to return.
        :param offset: Offset needed to return a specific subset of results.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.getCategories",
            params,
            response_model=responses.market.GetCategoriesResponse,
            raw_response=True,
        )


class MarketGetComments(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        item_id: int,
        need_likes: bool,
        start_comment_id: int,
        offset: int,
        count: int,
        sort: str,
        extended: bool,
        fields: typing.List,
    ) -> responses.market.GetComments:
        """ market.getComments
        From Vk Docs: Returns comments list for an item.
        Access from user token(s)
        :param owner_id: ID of an item owner community
        :param item_id: Item ID.
        :param need_likes: '1' — to return likes info.
        :param start_comment_id: ID of a comment to start a list from (details below).
        :param offset: 
        :param count: Number of results to return.
        :param sort: Sort order ('asc' — from old to new, 'desc' — from new to old)
        :param extended: '1' — comments will be returned as numbered objects, in addition lists of 'profiles' and 'groups' objects will be returned.
        :param fields: List of additional profile fields to return. See the [vk.com/dev/fields|details]
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.getComments", params, response_model=responses.market.GetComments
        )


class MarketRemoveFromAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, item_id: int, album_ids: typing.List
    ) -> responses.market.RemoveFromAlbum:
        """ market.removeFromAlbum
        From Vk Docs: Removes an item from one or multiple collections.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param album_ids: Collections IDs to remove item from.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.removeFromAlbum",
            params,
            response_model=responses.market.RemoveFromAlbum,
        )


class MarketReorderAlbums(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, album_id: int, before: int, after: int
    ) -> responses.market.ReorderAlbums:
        """ market.reorderAlbums
        From Vk Docs: Reorders the collections list.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param album_id: Collection ID.
        :param before: ID of a collection to place current collection before it.
        :param after: ID of a collection to place current collection after it.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.reorderAlbums",
            params,
            response_model=responses.market.ReorderAlbums,
        )


class MarketReorderItems(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, album_id: int, item_id: int, before: int, after: int
    ) -> responses.market.ReorderItems:
        """ market.reorderItems
        From Vk Docs: Changes item place in a collection.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param album_id: ID of a collection to reorder items in. Set 0 to reorder full items list.
        :param item_id: Item ID.
        :param before: ID of an item to place current item before it.
        :param after: ID of an item to place current item after it.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.reorderItems", params, response_model=responses.market.ReorderItems
        )


class MarketReport(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, item_id: int, reason: int
    ) -> responses.market.Report:
        """ market.report
        From Vk Docs: Sends a complaint to the item.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Item ID.
        :param reason: Complaint reason. Possible values: *'0' — spam,, *'1' — child porn,, *'2' — extremism,, *'3' — violence,, *'4' — drugs propaganda,, *'5' — adult materials,, *'6' — insult.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.report", params, response_model=responses.market.Report
        )


class MarketReportComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int, reason: int
    ) -> responses.market.ReportComment:
        """ market.reportComment
        From Vk Docs: Sends a complaint to the item's comment.
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param comment_id: Comment ID.
        :param reason: Complaint reason. Possible values: *'0' — spam,, *'1' — child porn,, *'2' — extremism,, *'3' — violence,, *'4' — drugs propaganda,, *'5' — adult materials,, *'6' — insult.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.reportComment",
            params,
            response_model=responses.market.ReportComment,
        )


class MarketRestore(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, item_id: int) -> responses.market.Restore:
        """ market.restore
        From Vk Docs: Restores recently deleted item
        Access from user token(s)
        :param owner_id: ID of an item owner community.
        :param item_id: Deleted item ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.restore", params, response_model=responses.market.Restore
        )


class MarketRestoreComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int
    ) -> responses.market.RestoreComment:
        """ market.restoreComment
        From Vk Docs: Restores a recently deleted comment
        Access from user token(s)
        :param owner_id: identifier of an item owner community, "Note that community id in the 'owner_id' parameter should be negative number. For example 'owner_id'=-1 matches the [vk.com/apiclub|VK API] community "
        :param comment_id: deleted comment id
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.restoreComment",
            params,
            response_model=responses.market.RestoreComment,
        )


class MarketSearch(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        album_id: int,
        q: str,
        price_from: int,
        price_to: int,
        tags: typing.List,
        sort: int,
        rev: int,
        offset: int,
        count: int,
        extended: bool,
        status: int,
    ) -> responses.market.Search:
        """ market.search
        From Vk Docs: Searches market items in a community's catalog
        Access from user token(s)
        :param owner_id: ID of an items owner community.
        :param album_id: 
        :param q: Search query, for example "pink slippers".
        :param price_from: Minimum item price value.
        :param price_to: Maximum item price value.
        :param tags: Comma-separated tag IDs list.
        :param sort: 
        :param rev: '0' — do not use reverse order, '1' — use reverse order
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of items to return.
        :param extended: '1' – to return additional fields: 'likes, can_comment, car_repost, photos'. By default: '0'.
        :param status: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request(
            "market.search", params, response_model=responses.market.Search
        )


class Market:
    def __init__(self, request):
        self.add = MarketAdd(request)
        self.add_album = MarketAddAlbum(request)
        self.add_to_album = MarketAddToAlbum(request)
        self.create_comment = MarketCreateComment(request)
        self.delete = MarketDelete(request)
        self.delete_album = MarketDeleteAlbum(request)
        self.delete_comment = MarketDeleteComment(request)
        self.edit = MarketEdit(request)
        self.edit_album = MarketEditAlbum(request)
        self.edit_comment = MarketEditComment(request)
        self.get = MarketGet(request)
        self.get_album_by_id = MarketGetAlbumById(request)
        self.get_albums = MarketGetAlbums(request)
        self.get_by_id = MarketGetById(request)
        self.get_categories = MarketGetCategories(request)
        self.get_comments = MarketGetComments(request)
        self.remove_from_album = MarketRemoveFromAlbum(request)
        self.reorder_albums = MarketReorderAlbums(request)
        self.reorder_items = MarketReorderItems(request)
        self.report = MarketReport(request)
        self.report_comment = MarketReportComment(request)
        self.restore = MarketRestore(request)
        self.restore_comment = MarketRestoreComment(request)
        self.search = MarketSearch(request)
