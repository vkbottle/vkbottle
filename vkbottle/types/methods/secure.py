# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class SecureAddAppEvent(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, user_id: int, activity_id: int, value: int):
        """ secure.addAppEvent
        From Vk Docs: Adds user activity information to an application
        Access from service token(s)
        :param user_id: ID of a user to save the data
        :param activity_id: there are 2 default activities: , * 1 – level. Works similar to ,, * 2 – points, saves points amount, Any other value is for saving completed missions
        :param value: depends on activity_id: * 1 – number, current level number,, * 2 – number, current user's points amount, , Any other value is ignored
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.addAppEvent", params)


class SecureCheckToken(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, token: str, ip: str):
        """ secure.checkToken
        From Vk Docs: Checks the user authentication in 'IFrame' and 'Flash' apps using the 'access_token' parameter.
        Access from service token(s)
        :param token: client 'access_token'
        :param ip: user 'ip address'. Note that user may access using the 'ipv6' address, in this case it is required to transmit the 'ipv6' address. If not transmitted, the address will not be checked.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.checkToken", params)


class SecureGetAppBalance(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self,):
        """ secure.getAppBalance
        From Vk Docs: Returns payment balance of the application in hundredth of a vote.
        Access from service token(s)
        
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.getAppBalance", params)


class SecureGetSMSHistory(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, user_id: int, date_from: int, date_to: int, limit: int):
        """ secure.getSMSHistory
        From Vk Docs: Shows a list of SMS notifications sent by the application using [vk.com/dev/secure.sendSMSNotification|secure.sendSMSNotification] method.
        Access from service token(s)
        :param user_id: 
        :param date_from: filter by start date. It is set as UNIX-time.
        :param date_to: filter by end date. It is set as UNIX-time.
        :param limit: number of returned posts. By default — 1000.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.getSMSHistory", params)


class SecureGetTransactionsHistory(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(
        self,
        type: int,
        uid_from: int,
        uid_to: int,
        date_from: int,
        date_to: int,
        limit: int,
    ):
        """ secure.getTransactionsHistory
        From Vk Docs: Shows history of votes transaction between users and the application.
        Access from service token(s)
        :param type: 
        :param uid_from: 
        :param uid_to: 
        :param date_from: 
        :param date_to: 
        :param limit: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.getTransactionsHistory", params)


class SecureGetUserLevel(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, user_ids: typing.List):
        """ secure.getUserLevel
        From Vk Docs: Returns one of the previously set game levels of one or more users in the application.
        Access from service token(s)
        :param user_ids: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.getUserLevel", params)


class SecureGiveEventSticker(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, user_ids: typing.List, achievement_id: int):
        """ secure.giveEventSticker
        From Vk Docs: Opens the game achievement and gives the user a sticker
        Access from service token(s)
        :param user_ids: 
        :param achievement_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.giveEventSticker", params)


class SecureSendNotification(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, user_ids: typing.List, user_id: int, message: str):
        """ secure.sendNotification
        From Vk Docs: Sends notification to the user.
        Access from service token(s)
        :param user_ids: 
        :param user_id: 
        :param message: notification text which should be sent in 'UTF-8' encoding ('254' characters maximum).
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.sendNotification", params)


class SecureSendSMSNotification(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(self, user_id: int, message: str):
        """ secure.sendSMSNotification
        From Vk Docs: Sends 'SMS' notification to a user's mobile device.
        Access from service token(s)
        :param user_id: ID of the user to whom SMS notification is sent. The user shall allow the application to send him/her notifications (, +1).
        :param message: 'SMS' text to be sent in 'UTF-8' encoding. Only Latin letters and numbers are allowed. Maximum size is '160' characters.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.sendSMSNotification", params)


class SecureSetCounter(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.SERVICE]

    async def __call__(
        self, counters: typing.List, user_id: int, counter: int, increment: bool
    ):
        """ secure.setCounter
        From Vk Docs: Sets a counter which is shown to the user in bold in the left menu.
        Access from service token(s)
        :param counters: 
        :param user_id: 
        :param counter: counter value.
        :param increment: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("secure.setCounter", params)


class Secure:
    def __init__(self, request):
        self.add_app_event = SecureAddAppEvent(request)
        self.check_token = SecureCheckToken(request)
        self.get_app_balance = SecureGetAppBalance(request)
        self.get_s_m_s_history = SecureGetSMSHistory(request)
        self.get_transactions_history = SecureGetTransactionsHistory(request)
        self.get_user_level = SecureGetUserLevel(request)
        self.give_event_sticker = SecureGiveEventSticker(request)
        self.send_notification = SecureSendNotification(request)
        self.send_s_m_s_notification = SecureSendSMSNotification(request)
        self.set_counter = SecureSetCounter(request)
