from ..types.message import Message
from ..api import Api
from ..handler import Handler
from ..utils import Logger
from .patcher import Patcher
from asyncio import AbstractEventLoop, ensure_future


class EventProcessor(object):
    api: Api
    on: Handler
    patcher: Patcher
    _logger: Logger
    __loop: AbstractEventLoop

    async def _private_message_processor(self, obj: dict):
        answer = Message(**obj, api=[self.api])

        for key in self.on.message.inner:
            if key.match(answer.text) is not None:
                matching = self.on.message.inner[key]

                validators_check = await self.patcher.check_validators(
                    check_object=matching,
                    keys=key.match(answer.text).groupdict())

                if validators_check is not None:
                    # [Feature] Async Use
                    # Added v0.19#master
                    ensure_future(
                        matching['call'](
                            answer,
                            **validators_check
                        ))

                    self._logger.debug(
                        'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                            matching['call'].__name__,
                            answer.from_id
                        )
                    )
                    return True

        if self.on.undefined_func:
            ensure_future(self.on.undefined_func(answer))
        else:
            self._logger.info('Add on-undefined message handler!')

