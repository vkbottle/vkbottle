# Handling-View

View являются блокирующими менеджерами хендлеров. Если `process_event` у view вернул `True` то другие view уже не будут проверяться

Процедура поиска view обрабатывающего ивент проста:

Сначала обрабатывается `process_view` который должен вернуть `boolean`-значение. Если вернулось `True` то поиск view прекращается и вызывается `handle_event` который отвечает за подбор хендлера

## register_middleware(BaseMiddleware)

Добавляет мидлварь в `view.middlewares`

## Написание view

!!! info "Примечание"
    View - это "большой хендлер", имплементирующий индивидуальную логику работы с мидлварями, стейт менеджером и производными хендлеров

Кастомные view нужны обычно для создания среды обработки какого-то ивента или группы ивентов

Посмотреть пример view для сообщений [можно здесь](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/dispatch/views/bot/message.py)

У каждого view существует минимум **4** атрибута:

* handlers - лист из `ABCHandler`
* middlewares - сет из классов `BaseMiddleware`
* middleware_instances - лист объектов `BaseMiddleware`, используется в `view.pre_middleware` и `view.post_middleware`
* handler_return_manager - `BaseReturnManager`

Из них **рекомендуются** 2 атрибута, `handlers` и `middlewares`

Эти атрибуты впоследствии рекомендуется использовать в `handle_event` для запуска мидлварей и поиска хендлера

```python
from vkbottle import ABCView, MiddlewareResponse
from vkbottle_types.events.bot_events import PollVoteNew

class VoteView(ABCView):
    def __init__(self):
        super().__init__()

    async def process_event(self, event: dict) -> bool:
        # Эта функция принимает ивент в форме словаря,
        # она должна определить подходит ли ивент под
        # текущий view или нет и вернуть соответствующее
        # boolean-значение
        return event["type"] == "poll_vote_new"

    async def handle_event(
        self, event: dict, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ):
        # Эта функция полностью обрабатывает
        # полученный ивент
        vote = PollVoteNew(**event)

        # Здесь можно обозначить стейт-каст
        # по определенному ключу для объекта
        vote.object.state_peer = await state_dispenser.cast(vote.object.user_id)

        # Здесь можно имплементировать стандартное поведение мидлварей
        # Например, если `pre_middleware` вернул что-либо, то в одном из
        # мидлварей был вызван `self.stop(...)` - обработка сразу останавливается
        mw_instances = await self.pre_middleware(vote)
        if mw_instances is None:
            return logger.info("Обработка остановлена, pre_middleware вернул ошибку")

        # `handlers` и `handle_responses` нужны для post мидлварей
        handlers = []
        handler_responses = []

        for handler in self.handlers:
            if not await handler.filter(vote):
                continue

            handler_responses.append(await handler.handle(vote))
            handlers.append(handler)

            if handler.blocking:
                break

        # Запуск post-мидлварей
        await self.post_middleware(mw_instances, handler_responses, handlers)
```

Поздравляю вы написали свой view! Теперь можно перейти к регистрации хендлеров, но для этого потребуется их создать, можно воспользоваться `FromFuncHandler`:

```python
from vkbottle.bot import Bot, rules, BotLabeler
from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle_types.events.bot_events import PollVoteNew
from typing import Dict


async def vote_up(vote: PollVoteNew):
    print(
        "{} со стейтом {} голосует за {}".format(
            vote.object.user_id, vote.object.state_peer, vote.object.option_id
        )
    )

async def vote_up_admin(vote: PollVoteNew):
    print("Админ проголосовал за {}", vote.object.option_id)

my_view = VoteView()
my_view.handlers = [
    FromFuncHandler(
        vote_up_admin,
        rules.FuncRule(lambda v: v.object.user_id in admin_ids),
    ),
    FromFuncHandler(vote_up),
]

class MyLabeler(BotLabeler):
    def views(self) -> Dict[str, "ABCView"]:
        # Из views должны быть возвращены все view которые
        # будут позже обрабатываться роутером
        return {"vote_view": my_view}

bot = Bot()
bot.labeler = MyLabeler()
admin_ids = [1]
```

Бот с `VoteView` готов
