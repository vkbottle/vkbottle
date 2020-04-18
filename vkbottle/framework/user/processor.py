import types
from asyncio import AbstractEventLoop
from re import sub
from vkbottle.utils import logger, init_bot_mention

from vbml import Patcher

from vkbottle.types.message import Message
from vkbottle.api import UserApi
from vkbottle.framework.framework.handler.user import Handler
from vkbottle.framework.framework.handler import MiddlewareExecutor
from vkbottle.framework.framework.branch import AbstractBranchGenerator, GeneratorType
from vkbottle.framework.framework.branch import Branch, ExitBranch
from vkbottle.utils.tools import get_attr


class AsyncHandleManager:
    api: UserApi
    on: Handler
    middleware: MiddlewareExecutor
    patcher: Patcher
    branch: AbstractBranchGenerator
    user_id: int
    loop: AbstractEventLoop
    _expand_models: bool

    async def _processor(self, update: dict, update_code: int, update_fields: list):
        for rule in self.on.rules:
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

    async def expand_data(self, code: int, data):
        if code in range(6):
            data.update(
                (await self.api.messages.get_by_id(message_ids=data["message_id"]))
                .items[0]
                .dict()
            )
        return data
