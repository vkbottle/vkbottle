# Middleware

Мидлварь должен имплементировать методы `pre` и/или `post`. `pre` вызывается до поиска хендлеров, а `post` после.

Мидлвари всегда распаковываются из `labeler`

Абстрактный класс для мидлварей - `BaseMiddleware`

Конструктор принимает ивент в качестве аргумента

`pre`/`post` не принимают аргументов, должны возвращать `None`:

* `self.stop(ошибка)` исполнение view срочно останавливается
* `self.send({ключ: значние})` в контекст добавляются аргументы (ключ - имя аргумента)

`BaseMiddleware`, имеет доступ к следующим атрибутам:

* `event: Union[BaseGroupEvent, BaseUserEvent]` (собственно ивент)
* `view: ABCView` (с которым был обработан ивент)
* `handle_responses: list` (все то что вернули хендлеры по порядку их исполнения)
* `handlers: List[ABCHandler]` (все хендлеры что были исполнены)

Более того, это не все атрибуты и функции `BaseMiddleware`

[Примеры смотреть здесь](https://github.com/vkbottle/vkbottle/blob/masterhttps://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py)
