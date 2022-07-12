# Request Rescheduler

Решедулеры нужны для того, чтобы отложить запрос к апи, который не удался по техническим причинам - например, ошибки серверов вконтакте.

Вызываются они из [валидаторов респонсов](response-validator.md)

Решедулер должен имплементировать всего один метод - асинхронный reschedule, который получает на вход:

* `ctx_api` - апи с которым выполнялся запрос
* `method` - метод
* `data` - переданные параметры
* `recent_response` - ответ (например: None)

## Пример

```python
import asyncio
from typing import TYPE_CHECKING, Any, Union

from vkbottle import ABCRequestRescheduler

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

class SomeRequestRescheduler(ABCRequestRescheduler):
    def __init__(self, delay: int = 1):
        self.delay = delay

    async def reschedule(
        self,
        ctx_api: Union["ABCAPI", "API"],
        method: str,
        data: dict,
        recent_response: Any,
    ) -> dict:
        await asyncio.sleep(self.delay)
        return await ctx_api.request(method, data)
```
