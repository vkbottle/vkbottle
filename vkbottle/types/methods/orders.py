# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class OrdersCancelSubscription(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, user_id: int, subscription_id: int, pending_cancel: bool):
        """ orders.cancelSubscription
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        :param subscription_id: 
        :param pending_cancel: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.cancelSubscription", params)


class OrdersChangeState(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, order_id: int, action: str, app_order_id: int, test_mode: bool
    ):
        """ orders.changeState
        From Vk Docs: Changes order status.
        Access from user, service token(s)
        :param order_id: order ID.
        :param action: action to be done with the order. Available actions: *cancel — to cancel unconfirmed order. *charge — to confirm unconfirmed order. Applies only if processing of [vk.com/dev/payments_status|order_change_state] notification failed. *refund — to cancel confirmed order.
        :param app_order_id: internal ID of the order in the application.
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.changeState", params)


class OrdersGet(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, offset: int, count: int, test_mode: bool):
        """ orders.get
        From Vk Docs: Returns a list of orders.
        Access from user, service token(s)
        :param offset: 
        :param count: number of returned orders.
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.get", params)


class OrdersGetAmount(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int, votes: typing.List):
        """ orders.getAmount
        From Vk Docs: 
        Access from user token(s)
        :param user_id: 
        :param votes: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.getAmount", params)


class OrdersGetById(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, order_id: int, order_ids: typing.List, test_mode: bool):
        """ orders.getById
        From Vk Docs: Returns information about orders by their IDs.
        Access from user, service token(s)
        :param order_id: order ID.
        :param order_ids: order IDs (when information about several orders is requested).
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.getById", params)


class OrdersGetUserSubscriptionById(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, user_id: int, subscription_id: int):
        """ orders.getUserSubscriptionById
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        :param subscription_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.getUserSubscriptionById", params)


class OrdersGetUserSubscriptions(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, user_id: int):
        """ orders.getUserSubscriptions
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.getUserSubscriptions", params)


class OrdersUpdateSubscription(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, user_id: int, subscription_id: int, price: int):
        """ orders.updateSubscription
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        :param subscription_id: 
        :param price: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("orders.updateSubscription", params)


class Orders:
    def __init__(self, request):
        self.cancel_subscription = OrdersCancelSubscription(request)
        self.change_state = OrdersChangeState(request)
        self.get = OrdersGet(request)
        self.get_amount = OrdersGetAmount(request)
        self.get_by_id = OrdersGetById(request)
        self.get_user_subscription_by_id = OrdersGetUserSubscriptionById(request)
        self.get_user_subscriptions = OrdersGetUserSubscriptions(request)
        self.update_subscription = OrdersUpdateSubscription(request)
