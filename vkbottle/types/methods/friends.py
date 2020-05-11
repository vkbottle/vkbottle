# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class FriendsAdd(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, text: str = None, follow: bool = None
    ) -> responses.friends.Add:
        """ friends.add
        From Vk Docs: Approves or creates a friend request.
        Access from user token(s)
        :param user_id: ID of the user whose friend request will be approved or to whom a friend request will be sent.
        :param text: Text of the message (up to 500 characters) for the friend request, if any.
        :param follow: '1' to pass an incoming request to followers list.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.add", params, response_model=responses.friends.AddModel
        )


class FriendsAddList(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, name: str, user_ids: typing.List = None
    ) -> responses.friends.AddList:
        """ friends.addList
        From Vk Docs: Creates a new friend list for the current user.
        Access from user token(s)
        :param name: Name of the friend list.
        :param user_ids: IDs of users to be added to the friend list.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.addList", params, response_model=responses.friends.AddListModel
        )


class FriendsAreFriends(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_ids: typing.List, need_sign: bool = None
    ) -> responses.friends.AreFriends:
        """ friends.areFriends
        From Vk Docs: Checks the current user's friendship status with other specified users.
        Access from user token(s)
        :param user_ids: IDs of the users whose friendship status to check.
        :param need_sign: '1' — to return 'sign' field. 'sign' is md5("{id}_{user_id}_{friends_status}_{application_secret}"), where id is current user ID. This field allows to check that data has not been modified by the client. By default: '0'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.areFriends",
            params,
            response_model=responses.friends.AreFriendsModel,
        )


class FriendsDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int = None) -> responses.friends.Delete:
        """ friends.delete
        From Vk Docs: Declines a friend request or deletes a user from the current user's friend list.
        Access from user token(s)
        :param user_id: ID of the user whose friend request is to be declined or who is to be deleted from the current user's friend list.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.delete", params, response_model=responses.friends.DeleteModel
        )


class FriendsDeleteAllRequests(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> responses.ok_response.OkResponse:
        """ friends.deleteAllRequests
        From Vk Docs: Marks all incoming friend requests as viewed.
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.deleteAllRequests",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FriendsDeleteList(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, list_id: int) -> responses.ok_response.OkResponse:
        """ friends.deleteList
        From Vk Docs: Deletes a friend list of the current user.
        Access from user token(s)
        :param list_id: ID of the friend list to delete.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.deleteList",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FriendsEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int, list_ids: typing.List = None
    ) -> responses.ok_response.OkResponse:
        """ friends.edit
        From Vk Docs: Edits the friend lists of the selected user.
        Access from user token(s)
        :param user_id: ID of the user whose friend list is to be edited.
        :param list_ids: IDs of the friend lists to which to add the user.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.edit", params, response_model=responses.ok_response.OkResponseModel
        )


class FriendsEditList(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        list_id: int,
        name: str = None,
        user_ids: typing.List = None,
        add_user_ids: typing.List = None,
        delete_user_ids: typing.List = None,
    ) -> responses.ok_response.OkResponse:
        """ friends.editList
        From Vk Docs: Edits a friend list of the current user.
        Access from user token(s)
        :param name: Name of the friend list.
        :param list_id: Friend list ID.
        :param user_ids: IDs of users in the friend list.
        :param add_user_ids: (Applies if 'user_ids' parameter is not set.), User IDs to add to the friend list.
        :param delete_user_ids: (Applies if 'user_ids' parameter is not set.), User IDs to delete from the friend list.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.editList",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class FriendsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        user_id: int = None,
        order: str = None,
        list_id: int = None,
        count: int = None,
        offset: int = None,
        fields: typing.List = None,
        name_case: str = None,
        ref: str = None,
    ) -> responses.friends.Get:
        """ friends.get
        From Vk Docs: Returns a list of user IDs or detailed information about a user's friends.
        Access from user, service token(s)
        :param user_id: User ID. By default, the current user ID.
        :param order: Sort order: , 'name' — by name (enabled only if the 'fields' parameter is used), 'hints' — by rating, similar to how friends are sorted in My friends section, , This parameter is available only for [vk.com/dev/standalone|desktop applications].
        :param list_id: ID of the friend list returned by the [vk.com/dev/friends.getLists|friends.getLists] method to be used as the source. This parameter is taken into account only when the uid parameter is set to the current user ID. This parameter is available only for [vk.com/dev/standalone|desktop applications].
        :param count: Number of friends to return.
        :param offset: Offset needed to return a specific subset of friends.
        :param fields: Profile fields to return. Sample values: 'uid', 'first_name', 'last_name', 'nickname', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'domain', 'has_mobile', 'rate', 'contacts', 'education'.
        :param name_case: Case for declension of user name and surname: , 'nom' — nominative (default) , 'gen' — genitive , 'dat' — dative , 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        :param ref: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.get", params, response_model=responses.friends.GetModel
        )


class FriendsGetAppUsers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> responses.friends.GetAppUsers:
        """ friends.getAppUsers
        From Vk Docs: Returns a list of IDs of the current user's friends who installed the application.
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getAppUsers",
            params,
            response_model=responses.friends.GetAppUsersModel,
        )


class FriendsGetByPhones(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, phones: typing.List = None, fields: typing.List = None
    ) -> responses.friends.GetByPhones:
        """ friends.getByPhones
        From Vk Docs: Returns a list of the current user's friends whose phone numbers, validated or specified in a profile, are in a given list.
        Access from user token(s)
        :param phones: List of phone numbers in MSISDN format (maximum 1000). Example: "+79219876543,+79111234567"
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'rate', 'contacts', 'education', 'online, counters'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getByPhones",
            params,
            response_model=responses.friends.GetByPhonesModel,
        )


class FriendsGetLists(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int = None, return_system: bool = None
    ) -> responses.friends.GetLists:
        """ friends.getLists
        From Vk Docs: Returns a list of the user's friend lists.
        Access from user token(s)
        :param user_id: User ID.
        :param return_system: '1' — to return system friend lists. By default: '0'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getLists", params, response_model=responses.friends.GetListsModel
        )


class FriendsGetMutual(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        source_uid: int = None,
        target_uid: int = None,
        target_uids: typing.List = None,
        order: str = None,
        count: int = None,
        offset: int = None,
    ) -> responses.friends.GetMutual:
        """ friends.getMutual
        From Vk Docs: Returns a list of user IDs of the mutual friends of two users.
        Access from user token(s)
        :param source_uid: ID of the user whose friends will be checked against the friends of the user specified in 'target_uid'.
        :param target_uid: ID of the user whose friends will be checked against the friends of the user specified in 'source_uid'.
        :param target_uids: IDs of the users whose friends will be checked against the friends of the user specified in 'source_uid'.
        :param order: Sort order: 'random' — random order
        :param count: Number of mutual friends to return.
        :param offset: Offset needed to return a specific subset of mutual friends.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getMutual", params, response_model=responses.friends.GetMutualModel
        )


class FriendsGetOnline(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        user_id: int = None,
        list_id: int = None,
        online_mobile: bool = None,
        order: str = None,
        count: int = None,
        offset: int = None,
    ) -> responses.friends.GetOnline:
        """ friends.getOnline
        From Vk Docs: Returns a list of user IDs of a user's friends who are online.
        Access from user token(s)
        :param user_id: User ID.
        :param list_id: Friend list ID. If this parameter is not set, information about all online friends is returned.
        :param online_mobile: '1' — to return an additional 'online_mobile' field, '0' — (default),
        :param order: Sort order: 'random' — random order
        :param count: Number of friends to return.
        :param offset: Offset needed to return a specific subset of friends.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getOnline", params, response_model=responses.friends.GetOnlineModel
        )


class FriendsGetRecent(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, count: int = None) -> responses.friends.GetRecent:
        """ friends.getRecent
        From Vk Docs: Returns a list of user IDs of the current user's recently added friends.
        Access from user token(s)
        :param count: Number of recently added friends to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getRecent", params, response_model=responses.friends.GetRecentModel
        )


class FriendsGetRequests(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        offset: int = None,
        count: int = None,
        extended: bool = None,
        need_mutual: bool = None,
        out: bool = None,
        sort: int = None,
        need_viewed: bool = None,
        suggested: bool = None,
        ref: str = None,
        fields: typing.List = None,
    ) -> responses.friends.GetRequests:
        """ friends.getRequests
        From Vk Docs: Returns information about the current user's incoming and outgoing friend requests.
        Access from user token(s)
        :param offset: Offset needed to return a specific subset of friend requests.
        :param count: Number of friend requests to return (default 100, maximum 1000).
        :param extended: '1' — to return response messages from users who have sent a friend request or, if 'suggested' is set to '1', to return a list of suggested friends
        :param need_mutual: '1' — to return a list of mutual friends (up to 20), if any
        :param out: '1' — to return outgoing requests, '0' — to return incoming requests (default)
        :param sort: Sort order: '1' — by number of mutual friends, '0' — by date
        :param need_viewed: 
        :param suggested: '1' — to return a list of suggested friends, '0' — to return friend requests (default)
        :param ref: 
        :param fields: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getRequests",
            params,
            response_model=responses.friends.GetRequestsModel,
        )


class FriendsGetSuggestions(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        filter: typing.List = None,
        count: int = None,
        offset: int = None,
        fields: typing.List = None,
        name_case: str = None,
    ) -> responses.friends.GetSuggestions:
        """ friends.getSuggestions
        From Vk Docs: Returns a list of profiles of users whom the current user may know.
        Access from user token(s)
        :param filter: Types of potential friends to return: 'mutual' — users with many mutual friends , 'contacts' — users found with the [vk.com/dev/account.importContacts|account.importContacts] method , 'mutual_contacts' — users who imported the same contacts as the current user with the [vk.com/dev/account.importContacts|account.importContacts] method
        :param count: Number of suggestions to return.
        :param offset: Offset needed to return a specific subset of suggestions.
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'rate', 'contacts', 'education', 'online', 'counters'.
        :param name_case: Case for declension of user name and surname: , 'nom' — nominative (default) , 'gen' — genitive , 'dat' — dative , 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.getSuggestions",
            params,
            response_model=responses.friends.GetSuggestionsModel,
        )


class FriendsSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        user_id: int,
        q: str = None,
        fields: typing.List = None,
        name_case: str = None,
        offset: int = None,
        count: int = None,
    ) -> responses.friends.Search:
        """ friends.search
        From Vk Docs: Returns a list of friends matching the search criteria.
        Access from user token(s)
        :param user_id: User ID.
        :param q: Search query string (e.g., 'Vasya Babich').
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'rate', 'contacts', 'education', 'online',
        :param name_case: Case for declension of user name and surname: 'nom' — nominative (default), 'gen' — genitive , 'dat' — dative, 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        :param offset: Offset needed to return a specific subset of friends.
        :param count: Number of friends to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "friends.search", params, response_model=responses.friends.SearchModel
        )


class Friends:
    def __init__(self, request):
        self.add = FriendsAdd(request)
        self.add_list = FriendsAddList(request)
        self.are_friends = FriendsAreFriends(request)
        self.delete = FriendsDelete(request)
        self.delete_all_requests = FriendsDeleteAllRequests(request)
        self.delete_list = FriendsDeleteList(request)
        self.edit = FriendsEdit(request)
        self.edit_list = FriendsEditList(request)
        self.get = FriendsGet(request)
        self.get_app_users = FriendsGetAppUsers(request)
        self.get_by_phones = FriendsGetByPhones(request)
        self.get_lists = FriendsGetLists(request)
        self.get_mutual = FriendsGetMutual(request)
        self.get_online = FriendsGetOnline(request)
        self.get_recent = FriendsGetRecent(request)
        self.get_requests = FriendsGetRequests(request)
        self.get_suggestions = FriendsGetSuggestions(request)
        self.search = FriendsSearch(request)
