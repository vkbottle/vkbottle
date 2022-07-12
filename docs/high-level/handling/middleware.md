# Middleware

Мидлварь должен имплементировать методы `pre` и/или `post`. `pre` вызывается до поиска хендлеров, а `post` после.

Мидлвари всегда распаковываются из `labeler`

Абстрактный класс для мидлварей - `BaseMiddleware`

Конструктор принимает ивент в качестве аргумента

`pre`/`post` не принимают аргументов, должны возвращать `None`:

* `self.stop(ошибка)` исполнение view срочно останавливается
* `self.send({ключ: значение})` в контекст добавляются аргументы (ключ - имя аргумента)

`BaseMiddleware`, имеет доступ к следующим атрибутам:

* `event` (сам евент, как указать его тип, смотрите ниже)
* `view: ABCView` (с которым был обработан ивент)
* `handle_responses: list` (все то что вернули хендлеры по порядку их исполнения)
* `handlers: List[ABCHandler]` (все хендлеры что были исполнены)

Тип ивента, который будет обрабатывать мидлварь, указывается в дженерике конструктора мидлвари. Например:

```python
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

class MyMiddleware(BaseMiddleware[Message]):
    ...
```

Для message_view это Message, а для raw_event_view словарь.

[Больше примеров можно посмотреть здесь](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py)
