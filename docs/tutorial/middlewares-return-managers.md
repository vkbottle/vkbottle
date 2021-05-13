# Мидлвари и return менеджеры

## Мидлвари

Мидлвари - так называемые внешние слои, покрывающие обработку хендлеров. У мидлварей есть два состояния - `pre` и `post`, `pre` это то, что происходит до начала поиска хендлера (когда только нашелся нужный `view`), а `post` - то что происходит когда хендлер уже был обработан и известно все о прошедшей обработке: какие хендлеры сработали, что они вернули

Чтобы сделать мидлварь импортируйте для начала абстрактный класс для него из корневого пакета:

```python
from vkbottle import BaseMiddleware
```

Теперь начните писать ваш собственный класс:

```python
class MiddlewareName(BaseMiddleware):
```

Middleware без методов `pre` или/и `post` бесполезен, нужно разобраться как реализировать каждый из них

### async def pre(self, event)

`pre` получает только ивент (например сообщение) и может вернуть `vkbottle.MiddlewareResponse` или `dict`

В этом акторе (в этой вами имплементированной функции) можно делать какие-то проверки. Если из pre вернется `MiddlewareResponse(False)` то обработка ивента на всех уровнях срочно прекратится, так можно например отсеивать какие-то спам сообщения или сообщения от игнорируемых пользователей.  
Если из мидлваря вернуть `dict`, то он будет распаковываться ВО ВСЕ ХЕНДЛЕРЫ (`await your_handler(event, **dict)`)

Вот так например можно отсеивать все сообщения от ботов:

```python
from vkbottle.bot import Message
from vkbottle import BaseMiddleware, MiddlewareResponse

class NoBotMiddleware(BaseMiddleware):
    async def pre(self, message: Message):
        if message.from_id < 0:
            return MiddlewareResponse(False)
```

### async def post(self, event, view, handle_responses, handlers)

`post` получает гораздо больше информации в отличии от `pre`, но он уже никак не может повлиять на обработку ивента. Обычно его используют для статистики и логов

```python
from vkbottle.bot import Message
from vkbottle import BaseMiddleware
from typing import List, Any

class LogMiddleware(BaseMiddleware):
    async def post(
        self,
        message: Message,
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
bot.labeler.message_view.register_middleware(NoBotMiddleware())
bot.labeler.message_view.register_middleware(LogMiddleware())
```

Кстати методом `register_middleware` можно пользоваться и как декоратором.

Полный код с мидлварями вы можете найти [в этом экзампле](/examples/high-level/middleware_example.py)

## Return менеджеры

В этой части туториала упомяналось о каких-то значениях, что возвращаются их хендлеров. Что же это и зачем они нужны?

> Создание кастомного менеджера для вашего view выходит за рамки этого туториала, но вы можете [прочитать об этом в технической документации](/docs/high-level/handling/view.md), когда посчитаете что готовы

Для общего понимания будет разобран return менеджер из коробки для `MessageView`

Суть заключается в том, что возвращая значения некоторых типов из хендлера, сработают хендлеры return менеджера которые произведут некоторые действия, вот что будет необходимо знать для комфортной разработки:

тип значения | что произойдет
--- | ---
str | строка отправится как сообщение
`tuple` или `list` | все элементы будут конвертированы в строки и отправлены как сообщения
dict | словарь распакуется как непозиционные аргументы для метода `message.answer`

## Экзамплы по этой части туториала

* [middleware](/examples/high-level/middleware_example.py)
