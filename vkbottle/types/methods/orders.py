# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class OrdersCancelSubscription(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, user_id: int, subscription_id: int, pending_cancel: bool = None
    ) -> responses.orders.CancelSubscription:
        """ orders.cancelSubscription
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        :param subscription_id: 
        :param pending_cancel: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.cancelSubscription",
            params,
            response_model=responses.orders.CancelSubscriptionModel,
        )


class OrdersChangeState(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        order_id: int,
        action: str,
        app_order_id: int = None,
        test_mode: bool = None,
    ) -> responses.orders.ChangeState:
        """ orders.changeState
        From Vk Docs: Changes order status.
        Access from user, service token(s)
        :param order_id: order ID.
        :param action: action to be done with the order. Available actions: *cancel — to cancel unconfirmed order. *charge — to confirm unconfirmed order. Applies only if processing of [vk.com/dev/payments_status|order_change_state] notification failed. *refund — to cancel confirmed order.
        :param app_order_id: internal ID of the order in the application.
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.changeState",
            params,
            response_model=responses.orders.ChangeStateModel,
        )


class OrdersGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, offset: int = None, count: int = None, test_mode: bool = None
    ) -> responses.orders.Get:
        """ orders.get
        From Vk Docs: Returns a list of orders.
        Access from user, service token(s)
        :param offset: 
        :param count: number of returned orders.
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.get", params, response_model=responses.orders.GetModel
        )


class OrdersGetAmount(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_id: int, votes: typing.List
    ) -> responses.orders.GetAmount:
        """ orders.getAmount
        From Vk Docs: 
        Access from user token(s)
        :param user_id: 
        :param votes: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.getAmount", params, response_model=responses.orders.GetAmountModel
        )


class OrdersGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        order_id: int = None,
        order_ids: typing.List = None,
        test_mode: bool = None,
    ) -> responses.orders.GetById:
        """ orders.getById
        From Vk Docs: Returns information about orders by their IDs.
        Access from user, service token(s)
        :param order_id: order ID.
        :param order_ids: order IDs (when information about several orders is requested).
        :param test_mode: if this parameter is set to 1, this method returns a list of test mode orders. By default — 0.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.getById", params, response_model=responses.orders.GetByIdModel
        )


class OrdersGetUserSubscriptionById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, user_id: int, subscription_id: int
    ) -> responses.orders.GetUserSubscriptionById:
        """ orders.getUserSubscriptionById
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        :param subscription_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.getUserSubscriptionById",
            params,
            response_model=responses.orders.GetUserSubscriptionByIdModel,
        )


class OrdersGetUserSubscriptions(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, user_id: int) -> responses.orders.GetUserSubscriptions:
        """ orders.getUserSubscriptions
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.getUserSubscriptions",
            params,
            response_model=responses.orders.GetUserSubscriptionsModel,
        )


class OrdersUpdateSubscription(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, user_id: int, price: int, subscription_id: int
    ) -> responses.orders.UpdateSubscription:
        """ orders.updateSubscription
        From Vk Docs: 
        Access from user, service token(s)
        :param user_id: 
        :param subscription_id: 
        :param price: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "orders.updateSubscription",
            params,
            response_model=responses.orders.UpdateSubscriptionModel,
        )


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
