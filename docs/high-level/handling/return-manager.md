# Return-Manager

Для каждого [view](view.md) можно установить `handler_return_manager`. Этот менеджер будет обрабатывать то, что возвращается из хендлеров.

По умолчанию менеджеры предустановлены в некоторых `view`.

Например, для сообщений:

* строка отправится в качестве текста сообщения
* каждый элемент кортежа или листа будет отправлен как сообщение
* словарь распакуется в метод отправки сообщения

Вот так выглядит его реализация:

```python
from vkbottle import BaseReturnManager
from vkbottle.bot import Message
from typing import Union


class BotMessageReturnHandler(BaseReturnManager):
    @BaseReturnManager.instance_of(str)
    async def str_handler(self, value: str, message: Message, _: dict):
        await message.answer(value)

    @BaseReturnManager.instance_of((tuple, list))
    async def iter_handler(self, value: Union[tuple, list], message: Message, _: dict):
        [await message.answer(str(e)) for e in value]

    @BaseReturnManager.instance_of(dict)
    async def dict_handler(self, value: dict, message: Message, _: dict):
        await message.answer(**value)
```

---

Первым аргументов в хендлер приходит само значение, что было получено из хендлера, вторым - объект ивента, третьим - данные из рулзов и мидлварей.

---

Хендлеры оборачиваются в декоратор `instance_of`, который принимает в качестве единственного аргумента тип или кортеж типов
