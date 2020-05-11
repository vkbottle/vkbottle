# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class PhotosConfirmTag(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: str, owner_id: int = None, tag_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.confirmTag
        From Vk Docs: Confirms a tag on a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param tag_id: Tag ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.confirmTag",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosCopy(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, photo_id: int, access_key: str = None
    ) -> responses.photos.Copy:
        """ photos.copy
        From Vk Docs: Allows to copy a photo to the "Saved photos" album
        Access from user token(s)
        :param owner_id: photo's owner ID
        :param photo_id: photo ID
        :param access_key: for private photos
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.copy", params, response_model=responses.photos.CopyModel
        )


class PhotosCreateAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        title: str,
        group_id: int = None,
        description: str = None,
        privacy_view: typing.List = None,
        privacy_comment: typing.List = None,
        upload_by_admins_only: bool = None,
        comments_disabled: bool = None,
    ) -> responses.photos.CreateAlbum:
        """ photos.createAlbum
        From Vk Docs: Creates an empty photo album.
        Access from user token(s)
        :param title: Album title.
        :param group_id: ID of the community in which the album will be created.
        :param description: Album description.
        :param privacy_view: 
        :param privacy_comment: 
        :param upload_by_admins_only: 
        :param comments_disabled: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.createAlbum",
            params,
            response_model=responses.photos.CreateAlbumModel,
        )


class PhotosCreateComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        photo_id: int,
        owner_id: int = None,
        message: str = None,
        attachments: typing.List = None,
        from_group: bool = None,
        reply_to_comment: int = None,
        sticker_id: int = None,
        access_key: str = None,
        guid: str = None,
    ) -> responses.photos.CreateComment:
        """ photos.createComment
        From Vk Docs: Adds a new comment on the photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param message: Comment text.
        :param attachments: (Required if 'message' is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — Media attachment owner ID. '<media_id>' — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        :param from_group: '1' — to post a comment from the community
        :param reply_to_comment: 
        :param sticker_id: 
        :param access_key: 
        :param guid: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.createComment",
            params,
            response_model=responses.photos.CreateCommentModel,
        )


class PhotosDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.delete
        From Vk Docs: Deletes a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.delete",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosDeleteAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, album_id: int, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.deleteAlbum
        From Vk Docs: Deletes a photo album belonging to the current user.
        Access from user token(s)
        :param album_id: Album ID.
        :param group_id: ID of the community that owns the album.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.deleteAlbum",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosDeleteComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, owner_id: int = None
    ) -> responses.photos.DeleteComment:
        """ photos.deleteComment
        From Vk Docs: Deletes a comment on the photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: Comment ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.deleteComment",
            params,
            response_model=responses.photos.DeleteCommentModel,
        )


class PhotosEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        photo_id: int,
        owner_id: int = None,
        caption: str = None,
        latitude: typing.Any = None,
        longitude: typing.Any = None,
        place_str: str = None,
        foursquare_id: str = None,
        delete_place: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ photos.edit
        From Vk Docs: Edits the caption of a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param caption: New caption for the photo. If this parameter is not set, it is considered to be equal to an empty string.
        :param latitude: 
        :param longitude: 
        :param place_str: 
        :param foursquare_id: 
        :param delete_place: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.edit", params, response_model=responses.ok_response.OkResponseModel
        )


class PhotosEditAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        album_id: int,
        title: str = None,
        description: str = None,
        owner_id: int = None,
        privacy_view: typing.List = None,
        privacy_comment: typing.List = None,
        upload_by_admins_only: bool = None,
        comments_disabled: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ photos.editAlbum
        From Vk Docs: Edits information about a photo album.
        Access from user token(s)
        :param album_id: ID of the photo album to be edited.
        :param title: New album title.
        :param description: New album description.
        :param owner_id: ID of the user or community that owns the album.
        :param privacy_view: 
        :param privacy_comment: 
        :param upload_by_admins_only: 
        :param comments_disabled: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.editAlbum",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosEditComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        comment_id: int,
        owner_id: int = None,
        message: str = None,
        attachments: typing.List = None,
    ) -> responses.ok_response.OkResponse:
        """ photos.editComment
        From Vk Docs: Edits a comment on a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: Comment ID.
        :param message: New text of the comment.
        :param attachments: (Required if 'message' is not set.) List of objects attached to the post, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — Media attachment owner ID. '<media_id>' — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.editComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        owner_id: int = None,
        album_id: str = None,
        photo_ids: typing.List = None,
        rev: bool = None,
        extended: bool = None,
        feed_type: str = None,
        feed: int = None,
        photo_sizes: bool = None,
        offset: int = None,
        count: int = None,
    ) -> responses.photos.Get:
        """ photos.get
        From Vk Docs: Returns a list of a user's or community's photos.
        Access from user, service token(s)
        :param owner_id: ID of the user or community that owns the photos. Use a negative value to designate a community ID.
        :param album_id: Photo album ID. To return information about photos from service albums, use the following string values: 'profile, wall, saved'.
        :param photo_ids: Photo IDs.
        :param rev: Sort order: '1' — reverse chronological, '0' — chronological
        :param extended: '1' — to return additional 'likes', 'comments', and 'tags' fields, '0' — (default)
        :param feed_type: Type of feed obtained in 'feed' field of the method.
        :param feed: unixtime, that can be obtained with [vk.com/dev/newsfeed.get|newsfeed.get] method in date field to get all photos uploaded by the user on a specific day, or photos the user has been tagged on. Also, 'uid' parameter of the user the event happened with shall be specified.
        :param photo_sizes: '1' — to return photo sizes in a [vk.com/dev/photo_sizes|special format]
        :param offset: 
        :param count: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.get", params, response_model=responses.photos.GetModel
        )


class PhotosGetAlbums(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        owner_id: int = None,
        album_ids: typing.List = None,
        offset: int = None,
        count: int = None,
        need_system: bool = None,
        need_covers: bool = None,
        photo_sizes: bool = None,
    ) -> responses.photos.GetAlbums:
        """ photos.getAlbums
        From Vk Docs: Returns a list of a user's or community's photo albums.
        Access from user, service token(s)
        :param owner_id: ID of the user or community that owns the albums.
        :param album_ids: Album IDs.
        :param offset: Offset needed to return a specific subset of albums.
        :param count: Number of albums to return.
        :param need_system: '1' — to return system albums with negative IDs
        :param need_covers: '1' — to return an additional 'thumb_src' field, '0' — (default)
        :param photo_sizes: '1' — to return photo sizes in a
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getAlbums", params, response_model=responses.photos.GetAlbumsModel
        )


class PhotosGetAlbumsCount(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, group_id: int = None
    ) -> responses.photos.GetAlbumsCount:
        """ photos.getAlbumsCount
        From Vk Docs: Returns the number of photo albums belonging to a user or community.
        Access from user token(s)
        :param user_id: User ID.
        :param group_id: Community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getAlbumsCount",
            params,
            response_model=responses.photos.GetAlbumsCountModel,
        )


class PhotosGetAll(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int = None,
        extended: bool = None,
        offset: int = None,
        count: int = None,
        photo_sizes: bool = None,
        no_service_albums: bool = None,
        need_hidden: bool = None,
        skip_hidden: bool = None,
    ) -> responses.photos.GetAll:
        """ photos.getAll
        From Vk Docs: Returns a list of photos belonging to a user or community, in reverse chronological order.
        Access from user token(s)
        :param owner_id: ID of a user or community that owns the photos. Use a negative value to designate a community ID.
        :param extended: '1' — to return detailed information about photos
        :param offset: Offset needed to return a specific subset of photos. By default, '0'.
        :param count: Number of photos to return.
        :param photo_sizes: '1' – to return image sizes in [vk.com/dev/photo_sizes|special format].
        :param no_service_albums: '1' – to return photos only from standard albums, '0' – to return all photos including those in service albums, e.g., 'My wall photos' (default)
        :param need_hidden: '1' – to show information about photos being hidden from the block above the wall.
        :param skip_hidden: '1' – not to return photos being hidden from the block above the wall. Works only with owner_id>0, no_service_albums is ignored.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getAll", params, response_model=responses.photos.GetAllModel
        )


class PhotosGetAllComments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int = None,
        album_id: int = None,
        need_likes: bool = None,
        offset: int = None,
        count: int = None,
    ) -> responses.photos.GetAllComments:
        """ photos.getAllComments
        From Vk Docs: Returns a list of comments on a specific photo album or all albums of the user sorted in reverse chronological order.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the album(s).
        :param album_id: Album ID. If the parameter is not set, comments on all of the user's albums will be returned.
        :param need_likes: '1' — to return an additional 'likes' field, '0' — (default)
        :param offset: Offset needed to return a specific subset of comments. By default, '0'.
        :param count: Number of comments to return. By default, '20'. Maximum value, '100'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getAllComments",
            params,
            response_model=responses.photos.GetAllCommentsModel,
        )


class PhotosGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, photos: typing.List, extended: bool = None, photo_sizes: bool = None
    ) -> responses.photos.GetById:
        """ photos.getById
        From Vk Docs: Returns information about photos by their IDs.
        Access from user, service token(s)
        :param photos: IDs separated with a comma, that are IDs of users who posted photos and IDs of photos themselves with an underscore character between such IDs. To get information about a photo in the group album, you shall specify group ID instead of user ID. Example: "1_129207899,6492_135055734, , -20629724_271945303"
        :param extended: '1' — to return additional fields, '0' — (default)
        :param photo_sizes: '1' — to return photo sizes in a
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getById", params, response_model=responses.photos.GetByIdModel
        )


class PhotosGetChatUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        chat_id: int,
        crop_x: int = None,
        crop_y: int = None,
        crop_width: int = None,
    ) -> responses.base.GetUploadServer:
        """ photos.getChatUploadServer
        From Vk Docs: Returns an upload link for chat cover pictures.
        Access from user token(s)
        :param chat_id: ID of the chat for which you want to upload a cover photo.
        :param crop_x: 
        :param crop_y: 
        :param crop_width: Width (in pixels) of the photo after cropping.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getChatUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class PhotosGetComments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        photo_id: int,
        owner_id: int = None,
        need_likes: bool = None,
        start_comment_id: int = None,
        offset: int = None,
        count: int = None,
        sort: str = None,
        access_key: str = None,
        extended: bool = None,
        fields: typing.List = None,
    ) -> responses.photos.GetComments:
        """ photos.getComments
        From Vk Docs: Returns a list of comments on a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param need_likes: '1' — to return an additional 'likes' field, '0' — (default)
        :param start_comment_id: 
        :param offset: Offset needed to return a specific subset of comments. By default, '0'.
        :param count: Number of comments to return.
        :param sort: Sort order: 'asc' — old first, 'desc' — new first
        :param access_key: 
        :param extended: 
        :param fields: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getComments",
            params,
            response_model=responses.photos.GetCommentsModel,
        )


class PhotosGetMarketAlbumUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int) -> responses.base.GetUploadServer:
        """ photos.getMarketAlbumUploadServer
        From Vk Docs: Returns the server address for market album photo upload.
        Access from user token(s)
        :param group_id: Community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getMarketAlbumUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class PhotosGetMarketUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        main_photo: bool = None,
        crop_x: int = None,
        crop_y: int = None,
        crop_width: int = None,
    ) -> responses.photos.GetMarketUploadServer:
        """ photos.getMarketUploadServer
        From Vk Docs: Returns the server address for market photo upload.
        Access from user token(s)
        :param group_id: Community ID.
        :param main_photo: '1' if you want to upload the main item photo.
        :param crop_x: X coordinate of the crop left upper corner.
        :param crop_y: Y coordinate of the crop left upper corner.
        :param crop_width: Width of the cropped photo in px.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getMarketUploadServer",
            params,
            response_model=responses.photos.GetMarketUploadServerModel,
        )


class PhotosGetMessagesUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int = None
    ) -> responses.photos.GetMessagesUploadServer:
        """ photos.getMessagesUploadServer
        From Vk Docs: Returns the server address for photo upload in a private message for a user.
        Access from user, group token(s)
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'Chat ID', e.g. '2000000001'. For community: '- Community ID', e.g. '-12345'. "
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getMessagesUploadServer",
            params,
            response_model=responses.photos.GetMessagesUploadServerModel,
        )


class PhotosGetNewTags(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, offset: int = None, count: int = None
    ) -> responses.photos.GetNewTags:
        """ photos.getNewTags
        From Vk Docs: Returns a list of photos with tags that have not been viewed.
        Access from user token(s)
        :param offset: Offset needed to return a specific subset of photos.
        :param count: Number of photos to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getNewTags", params, response_model=responses.photos.GetNewTagsModel
        )


class PhotosGetOwnerCoverPhotoUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        crop_x: int = None,
        crop_y: int = None,
        crop_x2: int = None,
        crop_y2: int = None,
    ) -> responses.base.GetUploadServer:
        """ photos.getOwnerCoverPhotoUploadServer
        From Vk Docs: Returns the server address for owner cover upload.
        Access from user, group token(s)
        :param group_id: ID of community that owns the album (if the photo will be uploaded to a community album).
        :param crop_x: X coordinate of the left-upper corner
        :param crop_y: Y coordinate of the left-upper corner
        :param crop_x2: X coordinate of the right-bottom corner
        :param crop_y2: Y coordinate of the right-bottom corner
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getOwnerCoverPhotoUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class PhotosGetOwnerPhotoUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int = None) -> responses.base.GetUploadServer:
        """ photos.getOwnerPhotoUploadServer
        From Vk Docs: Returns an upload server address for a profile or community photo.
        Access from user token(s)
        :param owner_id: identifier of a community or current user. "Note that community id must be negative. 'owner_id=1' – user, 'owner_id=-1' – community, "
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getOwnerPhotoUploadServer",
            params,
            response_model=responses.base.GetUploadServerModel,
        )


class PhotosGetTags(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: int, owner_id: int = None, access_key: str = None
    ) -> responses.photos.GetTags:
        """ photos.getTags
        From Vk Docs: Returns a list of tags on a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param access_key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getTags", params, response_model=responses.photos.GetTagsModel
        )


class PhotosGetUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int = None, album_id: int = None
    ) -> responses.photos.GetUploadServer:
        """ photos.getUploadServer
        From Vk Docs: Returns the server address for photo upload.
        Access from user token(s)
        :param group_id: ID of community that owns the album (if the photo will be uploaded to a community album).
        :param album_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getUploadServer",
            params,
            response_model=responses.photos.GetUploadServerModel,
        )


class PhotosGetUserPhotos(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        user_id: int = None,
        offset: int = None,
        count: int = None,
        extended: bool = None,
        sort: str = None,
    ) -> responses.photos.GetUserPhotos:
        """ photos.getUserPhotos
        From Vk Docs: Returns a list of photos in which a user is tagged.
        Access from user token(s)
        :param user_id: User ID.
        :param offset: Offset needed to return a specific subset of photos. By default, '0'.
        :param count: Number of photos to return. Maximum value is 1000.
        :param extended: '1' — to return an additional 'likes' field, '0' — (default)
        :param sort: Sort order: '1' — by date the tag was added in ascending order, '0' — by date the tag was added in descending order
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getUserPhotos",
            params,
            response_model=responses.photos.GetUserPhotosModel,
        )


class PhotosGetWallUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int = None
    ) -> responses.photos.GetWallUploadServer:
        """ photos.getWallUploadServer
        From Vk Docs: Returns the server address for photo upload onto a user's wall.
        Access from user token(s)
        :param group_id: ID of community to whose wall the photo will be uploaded.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.getWallUploadServer",
            params,
            response_model=responses.photos.GetWallUploadServerModel,
        )


class PhotosMakeCover(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: int, owner_id: int = None, album_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.makeCover
        From Vk Docs: Makes a photo into an album cover.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param album_id: Album ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.makeCover",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosMove(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, target_album_id: int, owner_id: int = None, photo_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.move
        From Vk Docs: Moves a photo from one album to another.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param target_album_id: ID of the album to which the photo will be moved.
        :param photo_id: Photo ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.move", params, response_model=responses.ok_response.OkResponseModel
        )


class PhotosPutTag(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        photo_id: int,
        owner_id: int = None,
        user_id: int = None,
        x: typing.Any = None,
        y: typing.Any = None,
        x2: typing.Any = None,
        y2: typing.Any = None,
    ) -> responses.photos.PutTag:
        """ photos.putTag
        From Vk Docs: Adds a tag on the photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param user_id: ID of the user to be tagged.
        :param x: Upper left-corner coordinate of the tagged area (as a percentage of the photo's width).
        :param y: Upper left-corner coordinate of the tagged area (as a percentage of the photo's height).
        :param x2: Lower right-corner coordinate of the tagged area (as a percentage of the photo's width).
        :param y2: Lower right-corner coordinate of the tagged area (as a percentage of the photo's height).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.putTag", params, response_model=responses.photos.PutTagModel
        )


class PhotosRemoveTag(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: int, owner_id: int = None, tag_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.removeTag
        From Vk Docs: Removes a tag from a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param tag_id: Tag ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.removeTag",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosReorderAlbums(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, album_id: int, owner_id: int = None, before: int = None, after: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.reorderAlbums
        From Vk Docs: Reorders the album in the list of user albums.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the album.
        :param album_id: Album ID.
        :param before: ID of the album before which the album in question shall be placed.
        :param after: ID of the album after which the album in question shall be placed.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.reorderAlbums",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosReorderPhotos(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: int, owner_id: int = None, before: int = None, after: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.reorderPhotos
        From Vk Docs: Reorders the photo in the list of photos of the user album.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param before: ID of the photo before which the photo in question shall be placed.
        :param after: ID of the photo after which the photo in question shall be placed.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.reorderPhotos",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosReport(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, photo_id: int, reason: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.report
        From Vk Docs: Reports (submits a complaint about) a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        :param reason: Reason for the complaint: '0' – spam, '1' – child pornography, '2' – extremism, '3' – violence, '4' – drug propaganda, '5' – adult material, '6' – insult, abuse
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.report",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosReportComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int, reason: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.reportComment
        From Vk Docs: Reports (submits a complaint about) a comment on a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: ID of the comment being reported.
        :param reason: Reason for the complaint: '0' – spam, '1' – child pornography, '2' – extremism, '3' – violence, '4' – drug propaganda, '5' – adult material, '6' – insult, abuse
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.reportComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosRestore(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, photo_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ photos.restore
        From Vk Docs: Restores a deleted photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param photo_id: Photo ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.restore",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class PhotosRestoreComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, owner_id: int = None
    ) -> responses.photos.RestoreComment:
        """ photos.restoreComment
        From Vk Docs: Restores a deleted comment on a photo.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the photo.
        :param comment_id: ID of the deleted comment.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.restoreComment",
            params,
            response_model=responses.photos.RestoreCommentModel,
        )


class PhotosSave(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        album_id: int = None,
        group_id: int = None,
        server: int = None,
        photos_list: str = None,
        hash: str = None,
        latitude: typing.Any = None,
        longitude: typing.Any = None,
        caption: str = None,
    ) -> responses.photos.Save:
        """ photos.save
        From Vk Docs: Saves photos after successful uploading.
        Access from user token(s)
        :param album_id: ID of the album to save photos to.
        :param group_id: ID of the community to save photos to.
        :param server: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param photos_list: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param latitude: Geographical latitude, in degrees (from '-90' to '90').
        :param longitude: Geographical longitude, in degrees (from '-180' to '180').
        :param caption: Text describing the photo. 2048 digits max.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.save", params, response_model=responses.photos.SaveModel
        )


class PhotosSaveMarketAlbumPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, server: int, photo: str, hash: str
    ) -> responses.photos.SaveMarketAlbumPhoto:
        """ photos.saveMarketAlbumPhoto
        From Vk Docs: Saves market album photos after successful uploading.
        Access from user token(s)
        :param group_id: Community ID.
        :param photo: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param server: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.saveMarketAlbumPhoto",
            params,
            response_model=responses.photos.SaveMarketAlbumPhotoModel,
        )


class PhotosSaveMarketPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        photo: str,
        hash: str,
        group_id: int = None,
        server: int = None,
        crop_data: str = None,
        crop_hash: str = None,
    ) -> responses.photos.SaveMarketPhoto:
        """ photos.saveMarketPhoto
        From Vk Docs: Saves market photos after successful uploading.
        Access from user token(s)
        :param group_id: Community ID.
        :param photo: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param server: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param crop_data: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param crop_hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.saveMarketPhoto",
            params,
            response_model=responses.photos.SaveMarketPhotoModel,
        )


class PhotosSaveMessagesPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, photo: str, server: int = None, hash: str = None
    ) -> responses.photos.SaveMessagesPhoto:
        """ photos.saveMessagesPhoto
        From Vk Docs: Saves a photo after being successfully uploaded. URL obtained with [vk.com/dev/photos.getMessagesUploadServer|photos.getMessagesUploadServer] method.
        Access from user, group token(s)
        :param photo: Parameter returned when the photo is [vk.com/dev/upload_files|uploaded to the server].
        :param server: 
        :param hash: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.saveMessagesPhoto",
            params,
            response_model=responses.photos.SaveMessagesPhotoModel,
        )


class PhotosSaveOwnerCoverPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, hash: str, photo: str
    ) -> responses.photos.SaveOwnerCoverPhoto:
        """ photos.saveOwnerCoverPhoto
        From Vk Docs: Saves cover photo after successful uploading.
        Access from user, group token(s)
        :param hash: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        :param photo: Parameter returned when photos are [vk.com/dev/upload_files|uploaded to server].
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.saveOwnerCoverPhoto",
            params,
            response_model=responses.photos.SaveOwnerCoverPhotoModel,
        )


class PhotosSaveOwnerPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, server: str = None, hash: str = None, photo: str = None
    ) -> responses.photos.SaveOwnerPhoto:
        """ photos.saveOwnerPhoto
        From Vk Docs: Saves a profile or community photo. Upload URL can be got with the [vk.com/dev/photos.getOwnerPhotoUploadServer|photos.getOwnerPhotoUploadServer] method.
        Access from user token(s)
        :param server: parameter returned after [vk.com/dev/upload_files|photo upload].
        :param hash: parameter returned after [vk.com/dev/upload_files|photo upload].
        :param photo: parameter returned after [vk.com/dev/upload_files|photo upload].
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.saveOwnerPhoto",
            params,
            response_model=responses.photos.SaveOwnerPhotoModel,
        )


class PhotosSaveWallPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        photo: str,
        user_id: int = None,
        group_id: int = None,
        server: int = None,
        hash: str = None,
        latitude: typing.Any = None,
        longitude: typing.Any = None,
        caption: str = None,
    ) -> responses.photos.SaveWallPhoto:
        """ photos.saveWallPhoto
        From Vk Docs: Saves a photo to a user's or community's wall after being uploaded.
        Access from user token(s)
        :param user_id: ID of the user on whose wall the photo will be saved.
        :param group_id: ID of community on whose wall the photo will be saved.
        :param photo: Parameter returned when the the photo is [vk.com/dev/upload_files|uploaded to the server].
        :param server: 
        :param hash: 
        :param latitude: Geographical latitude, in degrees (from '-90' to '90').
        :param longitude: Geographical longitude, in degrees (from '-180' to '180').
        :param caption: Text describing the photo. 2048 digits max.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.saveWallPhoto",
            params,
            response_model=responses.photos.SaveWallPhotoModel,
        )


class PhotosSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        q: str = None,
        lat: typing.Any = None,
        long: typing.Any = None,
        start_time: int = None,
        end_time: int = None,
        sort: int = None,
        offset: int = None,
        count: int = None,
        radius: int = None,
    ) -> responses.photos.Search:
        """ photos.search
        From Vk Docs: Returns a list of photos.
        Access from user, service token(s)
        :param q: Search query string.
        :param lat: Geographical latitude, in degrees (from '-90' to '90').
        :param long: Geographical longitude, in degrees (from '-180' to '180').
        :param start_time: 
        :param end_time: 
        :param sort: Sort order:
        :param offset: Offset needed to return a specific subset of photos.
        :param count: Number of photos to return.
        :param radius: Radius of search in meters (works very approximately). Available values: '10', '100', '800', '6000', '50000'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "photos.search", params, response_model=responses.photos.SearchModel
        )


class Photos:
    def __init__(self, request):
        self.confirm_tag = PhotosConfirmTag(request)
        self.copy = PhotosCopy(request)
        self.create_album = PhotosCreateAlbum(request)
        self.create_comment = PhotosCreateComment(request)
        self.delete = PhotosDelete(request)
        self.delete_album = PhotosDeleteAlbum(request)
        self.delete_comment = PhotosDeleteComment(request)
        self.edit = PhotosEdit(request)
        self.edit_album = PhotosEditAlbum(request)
        self.edit_comment = PhotosEditComment(request)
        self.get = PhotosGet(request)
        self.get_albums = PhotosGetAlbums(request)
        self.get_albums_count = PhotosGetAlbumsCount(request)
        self.get_all = PhotosGetAll(request)
        self.get_all_comments = PhotosGetAllComments(request)
        self.get_by_id = PhotosGetById(request)
        self.get_chat_upload_server = PhotosGetChatUploadServer(request)
        self.get_comments = PhotosGetComments(request)
        self.get_market_album_upload_server = PhotosGetMarketAlbumUploadServer(request)
        self.get_market_upload_server = PhotosGetMarketUploadServer(request)
        self.get_messages_upload_server = PhotosGetMessagesUploadServer(request)
        self.get_new_tags = PhotosGetNewTags(request)
        self.get_owner_cover_photo_upload_server = PhotosGetOwnerCoverPhotoUploadServer(
            request
        )
        self.get_owner_photo_upload_server = PhotosGetOwnerPhotoUploadServer(request)
        self.get_tags = PhotosGetTags(request)
        self.get_upload_server = PhotosGetUploadServer(request)
        self.get_user_photos = PhotosGetUserPhotos(request)
        self.get_wall_upload_server = PhotosGetWallUploadServer(request)
        self.make_cover = PhotosMakeCover(request)
        self.move = PhotosMove(request)
        self.put_tag = PhotosPutTag(request)
        self.remove_tag = PhotosRemoveTag(request)
        self.reorder_albums = PhotosReorderAlbums(request)
        self.reorder_photos = PhotosReorderPhotos(request)
        self.report = PhotosReport(request)
        self.report_comment = PhotosReportComment(request)
        self.restore = PhotosRestore(request)
        self.restore_comment = PhotosRestoreComment(request)
        self.save = PhotosSave(request)
        self.save_market_album_photo = PhotosSaveMarketAlbumPhoto(request)
        self.save_market_photo = PhotosSaveMarketPhoto(request)
        self.save_messages_photo = PhotosSaveMessagesPhoto(request)
        self.save_owner_cover_photo = PhotosSaveOwnerCoverPhoto(request)
        self.save_owner_photo = PhotosSaveOwnerPhoto(request)
        self.save_wall_photo = PhotosSaveWallPhoto(request)
        self.search = PhotosSearch(request)
