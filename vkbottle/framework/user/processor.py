from asyncio import AbstractEventLoop
import types
import traceback
from vkbottle.utils import logger

from vbml import Patcher

from vkbottle.api import UserApi
from vkbottle.exceptions import VKError
from vkbottle.types.user_longpoll import Message
from vkbottle.framework.framework.handler.user.handler import Handler
from vkbottle.framework.framework.error_handler import VKErrorHandler
from vkbottle.framework.framework.handler import MiddlewareExecutor
from vkbottle.framework.framework.branch import (
    AbstractBranchGenerator,
    Branch,
    ExitBranch,
)
from vkbottle.types.events import UserEvents


class AsyncHandleManager:
    api: UserApi
    on: Handler
    middleware: MiddlewareExecutor
    patcher: Patcher
    branch: AbstractBranchGenerator
    user_id: int
    loop: AbstractEventLoop
    _expand_models: bool
    error_handler: VKErrorHandler

    async def _event_processor(
        self, update: dict, update_code: int, update_fields: list
    ):
        for rule in self.on.event.rules:
            check = await rule.check(update)

            if check is not None:
                fields, _ = rule.data["data"], rule.data["name"]
                data = dict(zip(fields, update_fields))
                args, kwargs = [], {}

                if self._expand_models:
                    data.update(await self.expand_data(update_code, data))

                if rule.data.get("dataclass"):
                    data = rule.data.get("dataclass")(**data)

                if isinstance(check, tuple):
                    if all([await s_rule.check(data) for s_rule in check]):
                        args = [a for rule in check for a in rule.context.args]
                        kwargs = {
                            k: v
                            for rule in check
                            for k, v in rule.context.kwargs.items()
                        }
                    else:
                        continue

                task = await rule.call(data, *args, **kwargs)

                if task is not None:
                    await data(str(task))

    async def _processor(self, update: dict, update_code: int, update_fields: list):
        try:
            data = update, update_code, update_fields
            if update_code not in list(map(int, UserEvents)):
                logger.warning("Undefined event {}", update_code)
                return
            event = UserEvents(update_code)
            logger.debug("New event: {} {}", event, update)
            if event is UserEvents.new_message:
                return await self._message_processor(*data)
            return await self._event_processor(*data)
        except VKError as e:
            await self.error_handler.handle_error(e)
        except:
            logger.error(
                "While user polling worked error occurred \n\n{traceback}",
                traceback=traceback.format_exc(),
            )

    async def _message_processor(
        self, update: dict, update_code: int, update_fields: list
    ):
        for rule in self.on.message_rules:
            check = await rule.check(update)

            if check is not None:
                fields, _ = rule.data["data"], rule.data["name"]
                data = dict(zip(fields, update_fields))
                args, kwargs = [], {}
                middleware_args = []

                if self._expand_models:
                    data.update(await self.expand_data(update_code, data))

                message = Message(**data)

                if isinstance(check, tuple):
                    if all([await s_rule.check(message) for s_rule in check]):
                        args = [a for rule in check for a in rule.context.args]
                        kwargs = {
                            k: v
                            for rule in check
                            for k, v in rule.context.kwargs.items()
                        }
                    else:
                        continue

                async for mr in self.middleware.run_middleware(message):
                    if mr is False:
                        return
                    elif mr is not None:
                        middleware_args.append(mr)

                if message.peer_id in await self.branch.queue:
                    await self._branched_processor(message, middleware_args)
                    return

                task = await rule.call(message, *args, **kwargs)
                await self._handler_return(task, data)
                return task

    async def expand_data(self, code: int, data: dict) -> dict:
        if code in range(6):
            exp = (
                await self.api.messages.get_by_id(message_ids=data["message_id"])
            ).items
            if len(exp):
                data.update(exp[0].dict())
        return data

    async def _branched_processor(self, message: Message, middleware_args: list):
        logger.debug(
            '-> BRANCHED MESSAGE FROM {} TEXT "{}"',
            message.peer_id,
            message.text.replace("\n", " "),
        )

        disposal, branch = await self.branch.load(message.peer_id)

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
                await task(message, *middleware_args, *args, **kwargs),
                break

        logger.info(
            'New BRANCHED "{0}" compiled with branch <{2}> (from: {1})'.format(
                message.text.replace("\n", " "),
                message.from_id,
                '"{}" with {} kwargs'.format(
                    branch.key,
                    branch.context
                    if len(branch.context) < 100
                    else branch.context[1:99] + "...",
                ),
            )
        )

    async def _handler_return(self, handler_return, data: dict) -> bool:
        """
        Allows use returns in handlers and operates them
        :param handler_return:
        :param data:
        :return:
        """
        if isinstance(handler_return, Branch):
            await self.branch.add(
                data["peer_id"],
                handler_return.branch_name,
                **handler_return.branch_kwargs
            )
            return True
        elif isinstance(handler_return, ExitBranch):
            await self.branch.exit(data["peer_id"])
            return True
        elif handler_return is not None:
            await Message(**data)(str(handler_return))
        return False
