import types
import typing

from vkbottle.framework.framework import swear
from vkbottle.framework.framework.branch import (
    Branch,
    ExitBranch,
)
from vkbottle.framework.framework.handler import MiddlewareFlags
from vkbottle.framework.framework.handler.user.events import ADDITIONAL_FIELDS
from vkbottle.framework.framework.branch import GeneratorType
from vkbottle.framework.processor import ABCProcessor
from vkbottle.types.events import UserEvents
from vkbottle.types.user_longpoll import Message
from vkbottle.utils import logger

if typing.TYPE_CHECKING:
    from vkbottle.rule import AbstractRule
    from vkbottle.types import BaseModel


class UserProcessor(ABCProcessor):
    def __init__(self, user_id: int, expand_models: bool = False):
        self.user_id = user_id
        self.expand_models = expand_models

    @swear(Exception, just_log=True)
    async def parent_processor(
        self, update: dict, update_code: int, update_fields: typing.List[int],
    ) -> bool:
        """ Classify and distribute user polling events as message and not message
        #TODO Reduce difference
        :param update: full event
        :param update_code: first element from update
        :param update_fields: fields stack
        """
        data = update, update_code, update_fields

        if update_code not in list(map(int, UserEvents)):
            logger.warning("Undefined event {}", update_code)
            return

        event = UserEvents(update_code)
        logger.debug("New event: {} {}", event, update)

        if event is UserEvents.new_message:
            return await self.message_processor(*data)
        return await self.event_processor(*data)

    async def event_processor(
        self, update: dict, update_code: int, update_fields: typing.List[int],
    ) -> None:
        """ Process non-message events. Use first rule to make dataclass (noqa)
        Params described in parent_processor
        """
        data = None  # Data is expanded from the first rule containing dataclass (see UserEvents)
        # Middleware and branch workers are not supported for events (#10) #TODO

        for rule in self.handler.event.rules:
            check = await rule.check(update)

            if check is not None:

                if data is None:
                    fields, _ = rule.data["data"], rule.data["name"]
                    data = dict(zip(fields, update_fields))

                    if self.expand_models:
                        data.update(await self.expand_data(update_code, data))

                args, kwargs = [], {}
                event = rule.data.get("dataclass")(**data)

                if isinstance(check, tuple):
                    if isinstance(check, tuple):
                        check = await self.filter(event, check)
                        if not check:
                            continue
                        args, kwargs = check

                task = await rule.call(event, *args, **kwargs)
                await self.handler_return(task, data)
                break

    async def message_processor(
        self, update: dict, update_code: int, update_fields: typing.List[int],
    ) -> None:
        """ Process message events. Use base fields to make a dataclass
        Params described in parent_processor
        """
        # Expanding data
        fields = ("message_id", "flags", *ADDITIONAL_FIELDS)
        data = dict(zip(fields, update_fields))
        middleware_args = []

        if self.expand_models:
            data.update(await self.expand_data(update_code, data))

        message = Message(**data)

        # Executing middleware
        async for mr in self.middleware.run_middleware(
            message, flag=MiddlewareFlags.PRE
        ):
            if self.status.middleware_expressions:
                if mr is False:
                    return
                elif mr is not None:
                    middleware_args.append(mr)

        # Executing branch queue
        if message.dict()[self.branch.checkup_key.value] in await self.branch.queue:
            return await self.branch_processor(message, middleware_args)

        # Rule checkup
        for rules in self.handler.message_rules:
            rule = rules[0]  # API Complexity #FIXME
            check = await rule.check(update)

            if check is not None:
                args, kwargs = [], {}

                if isinstance(check, tuple):
                    check = await self.filter(message, check)
                    if not check:
                        continue
                    args, kwargs = check

                task = await rule.call(message, *args, **kwargs)
                await self.handler_return(task, data)
                break

        async for mr in self.middleware.run_middleware(
            message, flag=MiddlewareFlags.POST, *middleware_args
        ):
            logger.debug(f"POST Middleware handler returned: {mr}")

    async def expand_data(self, code: int, data: dict) -> dict:
        """ Expand data with important fields such as from_id. Can be disabled for API efficiency with:
        >>> UserProcessor.expand_models = False
        :param code: first field from event (event id)
        :param data: full data (signed with base fields)
        """
        if code in range(6):
            exp = (
                await self.api.messages.get_by_id(message_ids=data["message_id"])
            ).items
            if len(exp):
                data.update(exp[0].dict())
        return data

    @staticmethod
    async def filter(
        event: "BaseModel", check: typing.Tuple["AbstractRule"],
    ) -> typing.Union[bool, typing.Tuple[list, dict]]:
        # Use filters to affect to this execution manually
        if all([await rule.check(event) for rule in check]):
            args = [a for rule in check for a in rule.context.args]
            kwargs = {k: v for rule in check for k, v in rule.context.kwargs.items()}
            return args, kwargs
        return False

    async def branch_processor(self, message: Message, middleware_args: list):
        """ Process messages for users in branch storage
        #TODO Make a simple branch extendable processor
        #TODO Move middleware_args
        """
        branch_checkup_key = message.dict()[self.branch.checkup_key.value]
        logger.debug(
            '-> BRANCHED MESSAGE FROM {} TEXT "{}"',
            branch_checkup_key,
            message.text.replace("\n", " "),
        )

        disposal, branch = await self.branch.load(branch_checkup_key)
        edited = None

        for n, member in disposal.items():
            rules = member[1]
            for rule in rules:
                if not await rule(message):
                    break
            else:
                task = types.MethodType(member[0], branch)
                args = [a for rule in rules for a in rule.context.args]
                kwargs = {
                    k: v for rule in rules for k, v in rule.context.kwargs.items()
                }
                handler_return = await task(message, *middleware_args, *args, **kwargs)
                edited = await self.handler_return(handler_return, message.dict())
                break

        # FIXME
        if edited is False and self.branch.generator is GeneratorType.DATABASE:
            if branch_checkup_key in await self.branch.queue:
                logger.debug("Updating branch context")
                await self.branch.add(branch_checkup_key, branch.key, **branch.context)

        logger.info(
            'New BRANCHED "{0}" compiled with branch <{2}> (from: {1})'.format(
                message.text.replace("\n", " "), branch_checkup_key, repr(branch.key),
            )
        )

    async def handler_return(self, handler_return, data: dict) -> bool:
        """ Allows use returns in handlers and operates them
        #TODO (issue #84) make handler return manager
        :param handler_return:
        :param data:
        :return:
        """
        if isinstance(handler_return, Branch):
            await self.branch.add(
                data["peer_id"],
                handler_return.branch_name,
                **handler_return.branch_kwargs,
            )
            return True

        elif isinstance(handler_return, ExitBranch):
            await self.branch.exit(data["peer_id"])
            return True

        elif handler_return is not None:
            await Message(**data)(str(handler_return))

        return False
