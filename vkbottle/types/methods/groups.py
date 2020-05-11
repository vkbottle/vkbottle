# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class GroupsAddAddress(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        address: str,
        country_id: int,
        latitude: typing.Any,
        title: str,
        additional_address: str = None,
        city_id: int = None,
        metro_id: int = None,
        longitude: typing.Any = None,
        phone: str = None,
        work_info_status: str = None,
        timetable: str = None,
        is_main_address: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.addAddress
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        :param title: 
        :param address: 
        :param additional_address: 
        :param country_id: 
        :param city_id: 
        :param metro_id: 
        :param latitude: 
        :param longitude: 
        :param phone: 
        :param work_info_status: 
        :param timetable: 
        :param is_main_address: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.addAddress",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsAddCallbackServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, title: str, url: str, secret_key: str = None
    ) -> responses.groups.AddCallbackServer:
        """ groups.addCallbackServer
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        :param url: 
        :param title: 
        :param secret_key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.addCallbackServer",
            params,
            response_model=responses.groups.AddCallbackServerModel,
        )


class GroupsAddLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, link: str, text: str = None
    ) -> responses.groups.AddLink:
        """ groups.addLink
        From Vk Docs: Allows to add a link to the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param link: Link URL.
        :param text: Description text for the link.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.addLink", params, response_model=responses.groups.AddLinkModel
        )


class GroupsApproveRequest(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, user_id: int
    ) -> responses.ok_response.OkResponse:
        """ groups.approveRequest
        From Vk Docs: Allows to approve join request to the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param user_id: User ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.approveRequest",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsBan(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        owner_id: int = None,
        end_date: int = None,
        reason: int = None,
        comment: str = None,
        comment_visible: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.ban
        From Vk Docs: 
        Access from user token(s)
        :param group_id: 
        :param owner_id: 
        :param end_date: 
        :param reason: 
        :param comment: 
        :param comment_visible: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.ban", params, response_model=responses.ok_response.OkResponseModel
        )


class GroupsCreate(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        title: str,
        description: str = None,
        type: str = None,
        public_category: int = None,
        subtype: int = None,
    ) -> responses.groups.Create:
        """ groups.create
        From Vk Docs: Creates a new community.
        Access from user token(s)
        :param title: Community title.
        :param description: Community description (ignored for 'type' = 'public').
        :param type: Community type. Possible values: *'group' – group,, *'event' – event,, *'public' – public page
        :param public_category: Category ID (for 'type' = 'public' only).
        :param subtype: Public page subtype. Possible values: *'1' – place or small business,, *'2' – company, organization or website,, *'3' – famous person or group of people,, *'4' – product or work of art.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.create", params, response_model=responses.groups.CreateModel
        )


class GroupsDeleteCallbackServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, server_id: int
    ) -> responses.ok_response.OkResponse:
        """ groups.deleteCallbackServer
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        :param server_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.deleteCallbackServer",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsDeleteLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, link_id: int
    ) -> responses.ok_response.OkResponse:
        """ groups.deleteLink
        From Vk Docs: Allows to delete a link from the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param link_id: Link ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.deleteLink",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsDisableOnline(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, group_id: int) -> responses.ok_response.OkResponse:
        """ groups.disableOnline
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.disableOnline",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        title: str = None,
        description: str = None,
        screen_name: str = None,
        access: int = None,
        website: str = None,
        subject: str = None,
        email: str = None,
        phone: str = None,
        rss: str = None,
        event_start_date: int = None,
        event_finish_date: int = None,
        event_group_id: int = None,
        public_category: int = None,
        public_subcategory: int = None,
        public_date: str = None,
        wall: int = None,
        topics: int = None,
        photos: int = None,
        video: int = None,
        audio: int = None,
        links: bool = None,
        events: bool = None,
        places: bool = None,
        contacts: bool = None,
        docs: int = None,
        wiki: int = None,
        messages: bool = None,
        articles: bool = None,
        addresses: bool = None,
        age_limits: int = None,
        market: bool = None,
        market_comments: bool = None,
        market_country: typing.List = None,
        market_city: typing.List = None,
        market_currency: int = None,
        market_contact: int = None,
        market_wiki: int = None,
        obscene_filter: bool = None,
        obscene_stopwords: bool = None,
        obscene_words: typing.List = None,
        main_section: int = None,
        secondary_section: int = None,
        country: int = None,
        city: int = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.edit
        From Vk Docs: Edits a community.
        Access from user token(s)
        :param group_id: Community ID.
        :param title: Community title.
        :param description: Community description.
        :param screen_name: Community screen name.
        :param access: Community type. Possible values: *'0' – open,, *'1' – closed,, *'2' – private.
        :param website: Website that will be displayed in the community information field.
        :param subject: Community subject. Possible values: , *'1' – auto/moto,, *'2' – activity holidays,, *'3' – business,, *'4' – pets,, *'5' – health,, *'6' – dating and communication, , *'7' – games,, *'8' – IT (computers and software),, *'9' – cinema,, *'10' – beauty and fashion,, *'11' – cooking,, *'12' – art and culture,, *'13' – literature,, *'14' – mobile services and internet,, *'15' – music,, *'16' – science and technology,, *'17' – real estate,, *'18' – news and media,, *'19' – security,, *'20' – education,, *'21' – home and renovations,, *'22' – politics,, *'23' – food,, *'24' – industry,, *'25' – travel,, *'26' – work,, *'27' – entertainment,, *'28' – religion,, *'29' – family,, *'30' – sports,, *'31' – insurance,, *'32' – television,, *'33' – goods and services,, *'34' – hobbies,, *'35' – finance,, *'36' – photo,, *'37' – esoterics,, *'38' – electronics and appliances,, *'39' – erotic,, *'40' – humor,, *'41' – society, humanities,, *'42' – design and graphics.
        :param email: Organizer email (for events).
        :param phone: Organizer phone number (for events).
        :param rss: RSS feed address for import (available only to communities with special permission. Contact vk.com/support to get it.
        :param event_start_date: Event start date in Unixtime format.
        :param event_finish_date: Event finish date in Unixtime format.
        :param event_group_id: Organizer community ID (for events only).
        :param public_category: Public page category ID.
        :param public_subcategory: Public page subcategory ID.
        :param public_date: Founding date of a company or organization owning the community in "dd.mm.YYYY" format.
        :param wall: Wall settings. Possible values: *'0' – disabled,, *'1' – open,, *'2' – limited (groups and events only),, *'3' – closed (groups and events only).
        :param topics: Board topics settings. Possbile values: , *'0' – disabled,, *'1' – open,, *'2' – limited (for groups and events only).
        :param photos: Photos settings. Possible values: *'0' – disabled,, *'1' – open,, *'2' – limited (for groups and events only).
        :param video: Video settings. Possible values: *'0' – disabled,, *'1' – open,, *'2' – limited (for groups and events only).
        :param audio: Audio settings. Possible values: *'0' – disabled,, *'1' – open,, *'2' – limited (for groups and events only).
        :param links: Links settings (for public pages only). Possible values: *'0' – disabled,, *'1' – enabled.
        :param events: Events settings (for public pages only). Possible values: *'0' – disabled,, *'1' – enabled.
        :param places: Places settings (for public pages only). Possible values: *'0' – disabled,, *'1' – enabled.
        :param contacts: Contacts settings (for public pages only). Possible values: *'0' – disabled,, *'1' – enabled.
        :param docs: Documents settings. Possible values: *'0' – disabled,, *'1' – open,, *'2' – limited (for groups and events only).
        :param wiki: Wiki pages settings. Possible values: *'0' – disabled,, *'1' – open,, *'2' – limited (for groups and events only).
        :param messages: Community messages. Possible values: *'0' — disabled,, *'1' — enabled.
        :param articles: 
        :param addresses: 
        :param age_limits: Community age limits. Possible values: *'1' — no limits,, *'2' — 16+,, *'3' — 18+.
        :param market: Market settings. Possible values: *'0' – disabled,, *'1' – enabled.
        :param market_comments: market comments settings. Possible values: *'0' – disabled,, *'1' – enabled.
        :param market_country: Market delivery countries.
        :param market_city: Market delivery cities (if only one country is specified).
        :param market_currency: Market currency settings. Possbile values: , *'643' – Russian rubles,, *'980' – Ukrainian hryvnia,, *'398' – Kazakh tenge,, *'978' – Euro,, *'840' – US dollars
        :param market_contact: Seller contact for market. Set '0' for community messages.
        :param market_wiki: ID of a wiki page with market description.
        :param obscene_filter: Obscene expressions filter in comments. Possible values: , *'0' – disabled,, *'1' – enabled.
        :param obscene_stopwords: Stopwords filter in comments. Possible values: , *'0' – disabled,, *'1' – enabled.
        :param obscene_words: Keywords for stopwords filter.
        :param main_section: 
        :param secondary_section: 
        :param country: Country of the community.
        :param city: City of the community.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.edit", params, response_model=responses.ok_response.OkResponseModel
        )


class GroupsEditAddress(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        address_id: int,
        title: str = None,
        address: str = None,
        additional_address: str = None,
        country_id: int = None,
        city_id: int = None,
        metro_id: int = None,
        latitude: typing.Any = None,
        longitude: typing.Any = None,
        phone: str = None,
        work_info_status: str = None,
        timetable: str = None,
        is_main_address: bool = None,
    ) -> responses.groups.EditAddress:
        """ groups.editAddress
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        :param address_id: 
        :param title: 
        :param address: 
        :param additional_address: 
        :param country_id: 
        :param city_id: 
        :param metro_id: 
        :param latitude: 
        :param longitude: 
        :param phone: 
        :param work_info_status: 
        :param timetable: 
        :param is_main_address: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.editAddress",
            params,
            response_model=responses.groups.EditAddressModel,
        )


class GroupsEditCallbackServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        url: str,
        server_id: int,
        title: str,
        secret_key: str = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.editCallbackServer
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        :param server_id: 
        :param url: 
        :param title: 
        :param secret_key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.editCallbackServer",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsEditLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, link_id: int, text: str = None
    ) -> responses.ok_response.OkResponse:
        """ groups.editLink
        From Vk Docs: Allows to edit a link in the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param link_id: Link ID.
        :param text: New description text for the link.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.editLink",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsEditManager(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        user_id: int,
        role: str = None,
        is_contact: bool = None,
        contact_position: str = None,
        contact_phone: str = None,
        contact_email: str = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.editManager
        From Vk Docs: Allows to add, remove or edit the community manager.
        Access from user token(s)
        :param group_id: Community ID.
        :param user_id: User ID.
        :param role: Manager role. Possible values: *'moderator',, *'editor',, *'administrator'.
        :param is_contact: '1' — to show the manager in Contacts block of the community.
        :param contact_position: Position to show in Contacts block.
        :param contact_phone: Contact phone.
        :param contact_email: Contact e-mail.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.editManager",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsEnableOnline(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, group_id: int) -> responses.ok_response.OkResponse:
        """ groups.enableOnline
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.enableOnline",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        user_id: int = None,
        extended: bool = None,
        filter: typing.List = None,
        fields: typing.List = None,
        offset: int = None,
        count: int = None,
    ) -> responses.groups.Get:
        """ groups.get
        From Vk Docs: Returns a list of the communities to which a user belongs.
        Access from user token(s)
        :param user_id: User ID.
        :param extended: '1' — to return complete information about a user's communities, '0' — to return a list of community IDs without any additional fields (default),
        :param filter: Types of communities to return: 'admin' — to return communities administered by the user , 'editor' — to return communities where the user is an administrator or editor, 'moder' — to return communities where the user is an administrator, editor, or moderator, 'groups' — to return only groups, 'publics' — to return only public pages, 'events' — to return only events
        :param fields: Profile fields to return.
        :param offset: Offset needed to return a specific subset of communities.
        :param count: Number of communities to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.get", params, response_model=responses.groups.GetModel
        )


class GroupsGetAddresses(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        group_id: int,
        address_ids: typing.List = None,
        latitude: typing.Any = None,
        longitude: typing.Any = None,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
    ) -> responses.groups.GetAddresses:
        """ groups.getAddresses
        From Vk Docs: Returns a list of community addresses.
        Access from user, service token(s)
        :param group_id: ID or screen name of the community.
        :param address_ids: 
        :param latitude: Latitude of  the user geo position.
        :param longitude: Longitude of the user geo position.
        :param offset: Offset needed to return a specific subset of community addresses.
        :param count: Number of community addresses to return.
        :param fields: Address fields
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getAddresses",
            params,
            response_model=responses.groups.GetAddressesModel,
        )


class GroupsGetBanned(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
        owner_id: int = None,
    ) -> responses.groups.GetBanned:
        """ groups.getBanned
        From Vk Docs: Returns a list of users on a community blacklist.
        Access from user, group token(s)
        :param group_id: Community ID.
        :param offset: Offset needed to return a specific subset of users.
        :param count: Number of users to return.
        :param fields: 
        :param owner_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getBanned", params, response_model=responses.groups.GetBannedModel
        )


class GroupsGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        group_ids: typing.List = None,
        group_id: str = None,
        fields: typing.List = None,
    ) -> responses.groups.GetById:
        """ groups.getById
        From Vk Docs: Returns information about communities by their IDs.
        Access from user, group, service token(s)
        :param group_ids: IDs or screen names of communities.
        :param group_id: ID or screen name of the community.
        :param fields: Group fields to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getById", params, response_model=responses.groups.GetByIdModel
        )


class GroupsGetCallbackConfirmationCode(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int
    ) -> responses.groups.GetCallbackConfirmationCode:
        """ groups.getCallbackConfirmationCode
        From Vk Docs: Returns Callback API confirmation code for the community.
        Access from user, group token(s)
        :param group_id: Community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getCallbackConfirmationCode",
            params,
            response_model=responses.groups.GetCallbackConfirmationCodeModel,
        )


class GroupsGetCallbackServers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, server_ids: typing.List = None
    ) -> responses.groups.GetCallbackServers:
        """ groups.getCallbackServers
        From Vk Docs: 
        Access from user, group token(s)
        :param group_id: 
        :param server_ids: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getCallbackServers",
            params,
            response_model=responses.groups.GetCallbackServersModel,
        )


class GroupsGetCallbackSettings(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, server_id: int = None
    ) -> responses.groups.GetCallbackSettings:
        """ groups.getCallbackSettings
        From Vk Docs: Returns [vk.com/dev/callback_api|Callback API] notifications settings.
        Access from user, group token(s)
        :param group_id: Community ID.
        :param server_id: Server ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getCallbackSettings",
            params,
            response_model=responses.groups.GetCallbackSettingsModel,
        )


class GroupsGetCatalog(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, category_id: int = None, subcategory_id: int = None
    ) -> responses.groups.GetCatalog:
        """ groups.getCatalog
        From Vk Docs: Returns communities list for a catalog category.
        Access from user token(s)
        :param category_id: Category id received from [vk.com/dev/groups.getCatalogInfo|groups.getCatalogInfo].
        :param subcategory_id: Subcategory id received from [vk.com/dev/groups.getCatalogInfo|groups.getCatalogInfo].
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getCatalog", params, response_model=responses.groups.GetCatalogModel
        )


class GroupsGetCatalogInfo(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, extended: bool = None, subcategories: bool = None
    ) -> responses.groups.GetCatalogInfo:
        """ groups.getCatalogInfo
        From Vk Docs: Returns categories list for communities catalog
        Access from user token(s)
        :param extended: 1 – to return communities count and three communities for preview. By default: 0.
        :param subcategories: 1 – to return subcategories info. By default: 0.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getCatalogInfo",
            params,
            response_model=responses.groups.GetCatalogInfoModel,
        )


class GroupsGetInvitedUsers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
        name_case: str = None,
    ) -> responses.groups.GetInvitedUsers:
        """ groups.getInvitedUsers
        From Vk Docs: Returns invited users list of a community
        Access from user token(s)
        :param group_id: Group ID to return invited users for.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of results to return.
        :param fields: List of additional fields to be returned. Available values: 'sex, bdate, city, country, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, online_mobile, lists, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters'.
        :param name_case: Case for declension of user name and surname. Possible values: *'nom' — nominative (default),, *'gen' — genitive,, *'dat' — dative,, *'acc' — accusative, , *'ins' — instrumental,, *'abl' — prepositional.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getInvitedUsers",
            params,
            response_model=responses.groups.GetInvitedUsersModel,
        )


class GroupsGetInvites(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, offset: int = None, count: int = None, extended: bool = None
    ) -> responses.groups.GetInvites:
        """ groups.getInvites
        From Vk Docs: Returns a list of invitations to join communities and events.
        Access from user token(s)
        :param offset: Offset needed to return a specific subset of invitations.
        :param count: Number of invitations to return.
        :param extended: '1' — to return additional [vk.com/dev/fields_groups|fields] for communities..
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getInvites", params, response_model=responses.groups.GetInvitesModel
        )


class GroupsGetLongPollServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, group_id: int) -> responses.groups.GetLongPollServer:
        """ groups.getLongPollServer
        From Vk Docs: Returns the data needed to query a Long Poll server for events
        Access from user, group token(s)
        :param group_id: Community ID
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getLongPollServer",
            params,
            response_model=responses.groups.GetLongPollServerModel,
        )


class GroupsGetLongPollSettings(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, group_id: int) -> responses.groups.GetLongPollSettings:
        """ groups.getLongPollSettings
        From Vk Docs: Returns Long Poll notification settings
        Access from user, group token(s)
        :param group_id: Community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getLongPollSettings",
            params,
            response_model=responses.groups.GetLongPollSettingsModel,
        )


class GroupsGetMembers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        group_id: str = None,
        sort: str = None,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
        filter: str = None,
    ) -> responses.groups.GetMembers:
        """ groups.getMembers
        From Vk Docs: Returns a list of community members.
        Access from user, group, service token(s)
        :param group_id: ID or screen name of the community.
        :param sort: Sort order. Available values: 'id_asc', 'id_desc', 'time_asc', 'time_desc'. 'time_asc' and 'time_desc' are availavle only if the method is called by the group's 'moderator'.
        :param offset: Offset needed to return a specific subset of community members.
        :param count: Number of community members to return.
        :param fields: List of additional fields to be returned. Available values: 'sex, bdate, city, country, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, online_mobile, lists, domain, has_mobile, contacts, connections, site, education, universities, schools, can_post, can_see_all_posts, can_see_audio, can_write_private_message, status, last_seen, common_count, relation, relatives, counters'.
        :param filter: *'friends' – only friends in this community will be returned,, *'unsure' – only those who pressed 'I may attend' will be returned (if it's an event).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getMembers", params, response_model=responses.groups.GetMembersModel
        )


class GroupsGetRequests(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        offset: int = None,
        count: int = None,
        fields: typing.List = None,
    ) -> responses.groups.GetRequests:
        """ groups.getRequests
        From Vk Docs: Returns a list of requests to the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of results to return.
        :param fields: Profile fields to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getRequests",
            params,
            response_model=responses.groups.GetRequestsModel,
        )


class GroupsGetSettings(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int) -> responses.groups.GetSettings:
        """ groups.getSettings
        From Vk Docs: Returns community settings.
        Access from user token(s)
        :param group_id: Community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getSettings",
            params,
            response_model=responses.groups.GetSettingsModel,
        )


class GroupsGetTokenPermissions(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.GROUP]

    async def __call__(self,) -> responses.groups.GetTokenPermissions:
        """ groups.getTokenPermissions
        From Vk Docs: 
        Access from group token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.getTokenPermissions",
            params,
            response_model=responses.groups.GetTokenPermissionsModel,
        )


class GroupsInvite(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, user_id: int
    ) -> responses.ok_response.OkResponse:
        """ groups.invite
        From Vk Docs: Allows to invite friends to the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param user_id: User ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.invite",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsIsMember(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        group_id: str,
        user_id: int = None,
        user_ids: typing.List = None,
        extended: bool = None,
    ) -> responses.groups.IsMember:
        """ groups.isMember
        From Vk Docs: Returns information specifying whether a user is a member of a community.
        Access from user, group, service token(s)
        :param group_id: ID or screen name of the community.
        :param user_id: User ID.
        :param user_ids: User IDs.
        :param extended: '1' — to return an extended response with additional fields. By default: '0'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.isMember", params, response_model=responses.groups.IsMemberModel
        )


class GroupsJoin(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int = None, not_sure: str = None
    ) -> responses.ok_response.OkResponse:
        """ groups.join
        From Vk Docs: With this method you can join the group or public page, and also confirm your participation in an event.
        Access from user token(s)
        :param group_id: ID or screen name of the community.
        :param not_sure: Optional parameter which is taken into account when 'gid' belongs to the event: '1' — Perhaps I will attend, '0' — I will be there for sure (default), ,
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.join", params, response_model=responses.ok_response.OkResponseModel
        )


class GroupsLeave(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int) -> responses.ok_response.OkResponse:
        """ groups.leave
        From Vk Docs: With this method you can leave a group, public page, or event.
        Access from user token(s)
        :param group_id: ID or screen name of the community.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.leave", params, response_model=responses.ok_response.OkResponseModel
        )


class GroupsRemoveUser(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, user_id: int
    ) -> responses.ok_response.OkResponse:
        """ groups.removeUser
        From Vk Docs: Removes a user from the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param user_id: User ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.removeUser",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsReorderLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, link_id: int, after: int = None
    ) -> responses.ok_response.OkResponse:
        """ groups.reorderLink
        From Vk Docs: Allows to reorder links in the community.
        Access from user token(s)
        :param group_id: Community ID.
        :param link_id: Link ID.
        :param after: ID of the link after which to place the link with 'link_id'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.reorderLink",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        q: str,
        type: str = None,
        country_id: int = None,
        city_id: int = None,
        future: bool = None,
        market: bool = None,
        sort: int = None,
        offset: int = None,
        count: int = None,
    ) -> responses.groups.Search:
        """ groups.search
        From Vk Docs: Returns a list of communities matching the search criteria.
        Access from user token(s)
        :param q: Search query string.
        :param type: Community type. Possible values: 'group, page, event.'
        :param country_id: Country ID.
        :param city_id: City ID. If this parameter is transmitted, country_id is ignored.
        :param future: '1' — to return only upcoming events. Works with the 'type' = 'event' only.
        :param market: '1' — to return communities with enabled market only.
        :param sort: Sort order. Possible values: *'0' — default sorting (similar the full version of the site),, *'1' — by growth speed,, *'2'— by the "day attendance/members number" ratio,, *'3' — by the "Likes number/members number" ratio,, *'4' — by the "comments number/members number" ratio,, *'5' — by the "boards entries number/members number" ratio.
        :param offset: Offset needed to return a specific subset of results.
        :param count: Number of communities to return. "Note that you can not receive more than first thousand of results, regardless of 'count' and 'offset' values."
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.search", params, response_model=responses.groups.SearchModel
        )


class GroupsSetCallbackSettings(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        server_id: int = None,
        api_version: str = None,
        message_new: bool = None,
        message_reply: bool = None,
        message_allow: bool = None,
        message_edit: bool = None,
        message_deny: bool = None,
        message_typing_state: bool = None,
        photo_new: bool = None,
        audio_new: bool = None,
        video_new: bool = None,
        wall_reply_new: bool = None,
        wall_reply_edit: bool = None,
        wall_reply_delete: bool = None,
        wall_reply_restore: bool = None,
        wall_post_new: bool = None,
        wall_repost: bool = None,
        board_post_new: bool = None,
        board_post_edit: bool = None,
        board_post_restore: bool = None,
        board_post_delete: bool = None,
        photo_comment_new: bool = None,
        photo_comment_edit: bool = None,
        photo_comment_delete: bool = None,
        photo_comment_restore: bool = None,
        video_comment_new: bool = None,
        video_comment_edit: bool = None,
        video_comment_delete: bool = None,
        video_comment_restore: bool = None,
        market_comment_new: bool = None,
        market_comment_edit: bool = None,
        market_comment_delete: bool = None,
        market_comment_restore: bool = None,
        poll_vote_new: bool = None,
        group_join: bool = None,
        group_leave: bool = None,
        group_change_settings: bool = None,
        group_change_photo: bool = None,
        group_officers_edit: bool = None,
        user_block: bool = None,
        user_unblock: bool = None,
        lead_forms_new: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.setCallbackSettings
        From Vk Docs: Allow to set notifications settings for group.
        Access from user, group token(s)
        :param group_id: Community ID.
        :param server_id: Server ID.
        :param api_version: 
        :param message_new: A new incoming message has been received ('0' — disabled, '1' — enabled).
        :param message_reply: A new outcoming message has been received ('0' — disabled, '1' — enabled).
        :param message_allow: Allowed messages notifications ('0' — disabled, '1' — enabled).
        :param message_edit: 
        :param message_deny: Denied messages notifications ('0' — disabled, '1' — enabled).
        :param message_typing_state: 
        :param photo_new: New photos notifications ('0' — disabled, '1' — enabled).
        :param audio_new: New audios notifications ('0' — disabled, '1' — enabled).
        :param video_new: New videos notifications ('0' — disabled, '1' — enabled).
        :param wall_reply_new: New wall replies notifications ('0' — disabled, '1' — enabled).
        :param wall_reply_edit: Wall replies edited notifications ('0' — disabled, '1' — enabled).
        :param wall_reply_delete: A wall comment has been deleted ('0' — disabled, '1' — enabled).
        :param wall_reply_restore: A wall comment has been restored ('0' — disabled, '1' — enabled).
        :param wall_post_new: New wall posts notifications ('0' — disabled, '1' — enabled).
        :param wall_repost: New wall posts notifications ('0' — disabled, '1' — enabled).
        :param board_post_new: New board posts notifications ('0' — disabled, '1' — enabled).
        :param board_post_edit: Board posts edited notifications ('0' — disabled, '1' — enabled).
        :param board_post_restore: Board posts restored notifications ('0' — disabled, '1' — enabled).
        :param board_post_delete: Board posts deleted notifications ('0' — disabled, '1' — enabled).
        :param photo_comment_new: New comment to photo notifications ('0' — disabled, '1' — enabled).
        :param photo_comment_edit: A photo comment has been edited ('0' — disabled, '1' — enabled).
        :param photo_comment_delete: A photo comment has been deleted ('0' — disabled, '1' — enabled).
        :param photo_comment_restore: A photo comment has been restored ('0' — disabled, '1' — enabled).
        :param video_comment_new: New comment to video notifications ('0' — disabled, '1' — enabled).
        :param video_comment_edit: A video comment has been edited ('0' — disabled, '1' — enabled).
        :param video_comment_delete: A video comment has been deleted ('0' — disabled, '1' — enabled).
        :param video_comment_restore: A video comment has been restored ('0' — disabled, '1' — enabled).
        :param market_comment_new: New comment to market item notifications ('0' — disabled, '1' — enabled).
        :param market_comment_edit: A market comment has been edited ('0' — disabled, '1' — enabled).
        :param market_comment_delete: A market comment has been deleted ('0' — disabled, '1' — enabled).
        :param market_comment_restore: A market comment has been restored ('0' — disabled, '1' — enabled).
        :param poll_vote_new: A vote in a public poll has been added ('0' — disabled, '1' — enabled).
        :param group_join: Joined community notifications ('0' — disabled, '1' — enabled).
        :param group_leave: Left community notifications ('0' — disabled, '1' — enabled).
        :param group_change_settings: 
        :param group_change_photo: 
        :param group_officers_edit: 
        :param user_block: User added to community blacklist
        :param user_unblock: User removed from community blacklist
        :param lead_forms_new: New form in lead forms
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.setCallbackSettings",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsSetLongPollSettings(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        group_id: int,
        enabled: bool = None,
        api_version: str = None,
        message_new: bool = None,
        message_reply: bool = None,
        message_allow: bool = None,
        message_deny: bool = None,
        message_edit: bool = None,
        message_typing_state: bool = None,
        photo_new: bool = None,
        audio_new: bool = None,
        video_new: bool = None,
        wall_reply_new: bool = None,
        wall_reply_edit: bool = None,
        wall_reply_delete: bool = None,
        wall_reply_restore: bool = None,
        wall_post_new: bool = None,
        wall_repost: bool = None,
        board_post_new: bool = None,
        board_post_edit: bool = None,
        board_post_restore: bool = None,
        board_post_delete: bool = None,
        photo_comment_new: bool = None,
        photo_comment_edit: bool = None,
        photo_comment_delete: bool = None,
        photo_comment_restore: bool = None,
        video_comment_new: bool = None,
        video_comment_edit: bool = None,
        video_comment_delete: bool = None,
        video_comment_restore: bool = None,
        market_comment_new: bool = None,
        market_comment_edit: bool = None,
        market_comment_delete: bool = None,
        market_comment_restore: bool = None,
        poll_vote_new: bool = None,
        group_join: bool = None,
        group_leave: bool = None,
        group_change_settings: bool = None,
        group_change_photo: bool = None,
        group_officers_edit: bool = None,
        user_block: bool = None,
        user_unblock: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ groups.setLongPollSettings
        From Vk Docs: Sets Long Poll notification settings
        Access from user, group token(s)
        :param group_id: Community ID.
        :param enabled: Sets whether Long Poll is enabled ('0' — disabled, '1' — enabled).
        :param api_version: 
        :param message_new: A new incoming message has been received ('0' — disabled, '1' — enabled).
        :param message_reply: A new outcoming message has been received ('0' — disabled, '1' — enabled).
        :param message_allow: Allowed messages notifications ('0' — disabled, '1' — enabled).
        :param message_deny: Denied messages notifications ('0' — disabled, '1' — enabled).
        :param message_edit: A message has been edited ('0' — disabled, '1' — enabled).
        :param message_typing_state: 
        :param photo_new: New photos notifications ('0' — disabled, '1' — enabled).
        :param audio_new: New audios notifications ('0' — disabled, '1' — enabled).
        :param video_new: New videos notifications ('0' — disabled, '1' — enabled).
        :param wall_reply_new: New wall replies notifications ('0' — disabled, '1' — enabled).
        :param wall_reply_edit: Wall replies edited notifications ('0' — disabled, '1' — enabled).
        :param wall_reply_delete: A wall comment has been deleted ('0' — disabled, '1' — enabled).
        :param wall_reply_restore: A wall comment has been restored ('0' — disabled, '1' — enabled).
        :param wall_post_new: New wall posts notifications ('0' — disabled, '1' — enabled).
        :param wall_repost: New wall posts notifications ('0' — disabled, '1' — enabled).
        :param board_post_new: New board posts notifications ('0' — disabled, '1' — enabled).
        :param board_post_edit: Board posts edited notifications ('0' — disabled, '1' — enabled).
        :param board_post_restore: Board posts restored notifications ('0' — disabled, '1' — enabled).
        :param board_post_delete: Board posts deleted notifications ('0' — disabled, '1' — enabled).
        :param photo_comment_new: New comment to photo notifications ('0' — disabled, '1' — enabled).
        :param photo_comment_edit: A photo comment has been edited ('0' — disabled, '1' — enabled).
        :param photo_comment_delete: A photo comment has been deleted ('0' — disabled, '1' — enabled).
        :param photo_comment_restore: A photo comment has been restored ('0' — disabled, '1' — enabled).
        :param video_comment_new: New comment to video notifications ('0' — disabled, '1' — enabled).
        :param video_comment_edit: A video comment has been edited ('0' — disabled, '1' — enabled).
        :param video_comment_delete: A video comment has been deleted ('0' — disabled, '1' — enabled).
        :param video_comment_restore: A video comment has been restored ('0' — disabled, '1' — enabled).
        :param market_comment_new: New comment to market item notifications ('0' — disabled, '1' — enabled).
        :param market_comment_edit: A market comment has been edited ('0' — disabled, '1' — enabled).
        :param market_comment_delete: A market comment has been deleted ('0' — disabled, '1' — enabled).
        :param market_comment_restore: A market comment has been restored ('0' — disabled, '1' — enabled).
        :param poll_vote_new: A vote in a public poll has been added ('0' — disabled, '1' — enabled).
        :param group_join: Joined community notifications ('0' — disabled, '1' — enabled).
        :param group_leave: Left community notifications ('0' — disabled, '1' — enabled).
        :param group_change_settings: 
        :param group_change_photo: 
        :param group_officers_edit: 
        :param user_block: User added to community blacklist
        :param user_unblock: User removed from community blacklist
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.setLongPollSettings",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class GroupsUnban(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ groups.unban
        From Vk Docs: 
        Access from user token(s)
        :param group_id: 
        :param owner_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "groups.unban", params, response_model=responses.ok_response.OkResponseModel
        )


class Groups:
    def __init__(self, request):
        self.add_address = GroupsAddAddress(request)
        self.add_callback_server = GroupsAddCallbackServer(request)
        self.add_link = GroupsAddLink(request)
        self.approve_request = GroupsApproveRequest(request)
        self.ban = GroupsBan(request)
        self.create = GroupsCreate(request)
        self.delete_callback_server = GroupsDeleteCallbackServer(request)
        self.delete_link = GroupsDeleteLink(request)
        self.disable_online = GroupsDisableOnline(request)
        self.edit = GroupsEdit(request)
        self.edit_address = GroupsEditAddress(request)
        self.edit_callback_server = GroupsEditCallbackServer(request)
        self.edit_link = GroupsEditLink(request)
        self.edit_manager = GroupsEditManager(request)
        self.enable_online = GroupsEnableOnline(request)
        self.get = GroupsGet(request)
        self.get_addresses = GroupsGetAddresses(request)
        self.get_banned = GroupsGetBanned(request)
        self.get_by_id = GroupsGetById(request)
        self.get_callback_confirmation_code = GroupsGetCallbackConfirmationCode(request)
        self.get_callback_servers = GroupsGetCallbackServers(request)
        self.get_callback_settings = GroupsGetCallbackSettings(request)
        self.get_catalog = GroupsGetCatalog(request)
        self.get_catalog_info = GroupsGetCatalogInfo(request)
        self.get_invited_users = GroupsGetInvitedUsers(request)
        self.get_invites = GroupsGetInvites(request)
        self.get_long_poll_server = GroupsGetLongPollServer(request)
        self.get_long_poll_settings = GroupsGetLongPollSettings(request)
        self.get_members = GroupsGetMembers(request)
        self.get_requests = GroupsGetRequests(request)
        self.get_settings = GroupsGetSettings(request)
        self.get_token_permissions = GroupsGetTokenPermissions(request)
        self.invite = GroupsInvite(request)
        self.is_member = GroupsIsMember(request)
        self.join = GroupsJoin(request)
        self.leave = GroupsLeave(request)
        self.remove_user = GroupsRemoveUser(request)
        self.reorder_link = GroupsReorderLink(request)
        self.search = GroupsSearch(request)
        self.set_callback_settings = GroupsSetCallbackSettings(request)
        self.set_long_poll_settings = GroupsSetLongPollSettings(request)
        self.unban = GroupsUnban(request)
