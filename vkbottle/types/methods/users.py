# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class UsersGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        user_ids: typing.List = None,
        fields: typing.List = None,
        name_case: str = None,
    ) -> responses.users.Get:
        """ users.get
        From Vk Docs: Returns detailed information on users.
        Access from user, group, service token(s)
        :param user_ids: User IDs or screen names ('screen_name'). By default, current user ID.
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'contacts', 'education', 'online', 'counters', 'relation', 'last_seen', 'activity', 'can_write_private_message', 'can_see_all_posts', 'can_post', 'universities',
        :param name_case: Case for declension of user name and surname: 'nom' — nominative (default), 'gen' — genitive , 'dat' — dative, 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.get", params, response_model=responses.users.GetModel
        )


class UsersGetFollowers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        user_id: int = None,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
        name_case: str = None,
    ) -> responses.users.GetFollowers:
        """ users.getFollowers
        From Vk Docs: Returns a list of IDs of followers of the user in question, sorted by date added, most recent first.
        Access from user, service token(s)
        :param user_id: User ID.
        :param offset: Offset needed to return a specific subset of followers.
        :param count: Number of followers to return.
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'rate', 'contacts', 'education', 'online'.
        :param name_case: Case for declension of user name and surname: 'nom' — nominative (default), 'gen' — genitive , 'dat' — dative, 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.getFollowers",
            params,
            response_model=responses.users.GetFollowersModel,
        )


class UsersGetSubscriptions(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        user_id: int = None,
        extended: bool = None,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
    ) -> responses.users.GetSubscriptions:
        """ users.getSubscriptions
        From Vk Docs: Returns a list of IDs of users and communities followed by the user.
        Access from user, service token(s)
        :param user_id: User ID.
        :param extended: '1' — to return a combined list of users and communities, '0' — to return separate lists of users and communities (default)
        :param offset: Offset needed to return a specific subset of subscriptions.
        :param count: Number of users and communities to return.
        :param fields: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.getSubscriptions",
            params,
            response_model=responses.users.GetSubscriptionsModel,
        )


class UsersIsAppUser(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int = None) -> responses.users.IsAppUser:
        """ users.isAppUser
        From Vk Docs: Returns information whether a user installed the application.
        Access from user token(s)
        :param user_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.isAppUser", params, response_model=responses.users.IsAppUserModel
        )


class UsersReport(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int, type: str, comment: str = None
    ) -> responses.ok_response.OkResponse:
        """ users.report
        From Vk Docs: Reports (submits a complain about) a user.
        Access from user token(s)
        :param user_id: ID of the user about whom a complaint is being made.
        :param type: Type of complaint: 'porn' – pornography, 'spam' – spamming, 'insult' – abusive behavior, 'advertisement' – disruptive advertisements
        :param comment: Comment describing the complaint.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.report", params, response_model=responses.ok_response.OkResponseModel
        )


class UsersSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        q: str = None,
        sort: int = None,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
        city: int = None,
        country: int = None,
        hometown: str = None,
        university_country: int = None,
        university: int = None,
        university_year: int = None,
        university_faculty: int = None,
        university_chair: int = None,
        sex: int = None,
        status: int = None,
        age_from: int = None,
        age_to: int = None,
        birth_day: int = None,
        birth_month: int = None,
        birth_year: int = None,
        online: bool = None,
        has_photo: bool = None,
        school_country: int = None,
        school_city: int = None,
        school_class: int = None,
        school: int = None,
        school_year: int = None,
        religion: str = None,
        interests: str = None,
        company: str = None,
        position: str = None,
        group_id: int = None,
        from_list: typing.List = None,
    ) -> responses.users.Search:
        """ users.search
        From Vk Docs: Returns a list of users matching the search criteria.
        Access from user token(s)
        :param q: Search query string (e.g., 'Vasya Babich').
        :param sort: Sort order: '1' — by date registered, '0' — by rating
        :param offset: Offset needed to return a specific subset of users.
        :param count: Number of users to return.
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'rate', 'contacts', 'education', 'online',
        :param city: City ID.
        :param country: Country ID.
        :param hometown: City name in a string.
        :param university_country: ID of the country where the user graduated.
        :param university: ID of the institution of higher education.
        :param university_year: Year of graduation from an institution of higher education.
        :param university_faculty: Faculty ID.
        :param university_chair: Chair ID.
        :param sex: '1' — female, '2' — male, '0' — any (default)
        :param status: Relationship status: '1' — Not married, '2' — In a relationship, '3' — Engaged, '4' — Married, '5' — It's complicated, '6' — Actively searching, '7' — In love
        :param age_from: Minimum age.
        :param age_to: Maximum age.
        :param birth_day: Day of birth.
        :param birth_month: Month of birth.
        :param birth_year: Year of birth.
        :param online: '1' — online only, '0' — all users
        :param has_photo: '1' — with photo only, '0' — all users
        :param school_country: ID of the country where users finished school.
        :param school_city: ID of the city where users finished school.
        :param school_class: 
        :param school: ID of the school.
        :param school_year: School graduation year.
        :param religion: Users' religious affiliation.
        :param interests: Users' interests.
        :param company: Name of the company where users work.
        :param position: Job position.
        :param group_id: ID of a community to search in communities.
        :param from_list: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.search", params, response_model=responses.users.SearchModel
        )


class UsersSetCovidStatus(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.COVID]

    async def __call__(self, status_id: int) -> responses.ok_response.OkResponse:
        """
        Set special Covid emoji
        :param status_id: special status ID
        """
        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "users.setCovidStatus",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Users:
    def __init__(self, request):
        self.get = UsersGet(request)
        self.get_followers = UsersGetFollowers(request)
        self.get_subscriptions = UsersGetSubscriptions(request)
        self.is_app_user = UsersIsAppUser(request)
        self.report = UsersReport(request)
        self.search = UsersSearch(request)
        self.set_covid_status = UsersSetCovidStatus(request)
