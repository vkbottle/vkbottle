# Мидлвари и return менеджеры

## Мидлвари

Мидлвари - так называемые внешние слои, покрывающие обработку хендлеров. У мидлварей есть два состояния - `pre` и `post`, `pre` это то, что происходит до начала поиска хендлера (когда только нашелся нужный `view`), а `post` - то что происходит когда хендлер уже был обработан и известно все о прошедшей обработке: какие хендлеры сработали, что они вернули

Чтобы сделать мидлварь импортируйте для начала абстрактный класс для него из корневого пакета:

```python
from vkbottle import BaseMiddleware
from vkbottle.bot import Message
```

Теперь начните писать ваш собственный класс:

```python
class MiddlewareName(BaseMiddleware[Message]):
```
Так как наш мидлварь обрабатывает именно сообщения, нужно указать тип в дженерике.
В данном случае мы используем класс `Message` из `vkbottle.bot`

Middleware без методов `pre` или/и `post` бесполезен, нужно разобраться как реализовать каждый из них

### async def pre(self)

`pre` получает имеет доступен к ивенту (например сообщение) через `self` и может вернуть вызвать ошибку через `self.stop` или обновить констекст через `self.send`

[техническая документация](/docs/high-level/handling/middleware.md)

Вот так например можно отсеивать все сообщения от ботов:

```python
from vkbottle.bot import Message
from vkbottle import BaseMiddleware, MiddlewareResponse

class NoBotMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("from_id меньше 0")
```

### async def post(self, view, handle_responses, handlers)

`post` получает гораздо больше информации в отличии от `pre`, но он уже никак не может повлиять на обработку ивента. Обычно его используют для статистики и логов

```python
from vkbottle.bot import Message
from vkbottle import BaseMiddleware
from typing import List, Any

class LogMiddleware(BaseMiddleware[Message]):
    async def post(
        self,
        view: "ABCView",
        handle_responses: List[Any],
        handlers: List["ABCHandler"],
    ):
        if not handlers:
            return

        print(f"{len(handlers)} хендлеров сработало на сообщение. "
              f"Они вернули {handle_responses}, "
              f"все они принадлежали к view {view}")
```

---

`pre` и `post` можно использовать и одновременно в одном мидлваре

### Регистрация мидлварей

Чтобы зарегистрировать мидлварь (и он работал) нужно определиться с view к которому он принадлежит, в данном случае это `MessageView`

В лейблере `MessageView` располагается по адресу `.message_view`

У каждого view есть метод `register_middleware`, воспользуемся им:

```python
bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.labeler.message_view.register_middleware(LogMiddleware)
```

Кстати методом `register_middleware` можно пользоваться и как декоратором.

Полный код с мидлварями вы можете найти [в этом экзампле](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py)

## Return менеджеры

В этой части туториала упомяналось о каких-то значениях, что возвращаются их хендлеров. Что же это и зачем они нужны?

> Создание кастомного менеджера для вашего view выходит за рамки этого туториала, но вы можете [прочитать об этом в технической документации](/docs/high-level/handling/view.md), когда посчитаете что готовы

Для общего понимания будет разобран return менеджер из коробки для `MessageView`

Суть заключается в том, что возвращая значения некоторых типов из хендлера, сработают хендлеры return менеджера которые произведут некоторые действия, вот что будет необходимо знать для комфортной разработки:

| тип значения       | что произойдет                                                              |
| ------------------ | --------------------------------------------------------------------------- |
| str                | строка отправится как сообщение                                             |
| `tuple` или `list` | все элементы будут конвертированы в строки и отправлены как сообщения       |
| dict               | словарь распакуется как непозиционные аргументы для метода `message.answer` |

## Экзамплы по этой части туториала

* [middleware](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py)
