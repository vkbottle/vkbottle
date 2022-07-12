# Разделение кода

!!! info "Примечание"
    Разделение кода - очень важная вещь для создания структуры проекта

Чтобы делать это, в vkbottle предусмотрен инструмент `Blueprint`.

`Blueprint` - точная копия (в данном случае бота), но при всей идентичности с интерфейсом бота, блупринт не может быть индивидуально запущен как агент поллинга, он может лишь имплементировать хендлеры и другие `labeler` definition'ы

Атрибуты `api`, `polling` и `state_dispenser` могут быть использованы только в среде (хендлера например), до момента того, как блупринт был сконструирован они равны `None`, для определения сконструирован блупринт или нет в среде в которой находитесь вы, вы можете использовать атрибут `constructed`

Разделение кода, кроме того может быть очень грамотно использовано для создания локальных изменений в аплоадере, например `auto_rules` поможет установить правила, которые будут накладываться на все хендлеры сообщений блупринта

!!! warning "Внимание"
    `auto_rules` распространяется только на хендлеры сообщений, для сырых евентов вам нужен `raw_event_auto_rules` и кастомные правила, работающие с ними

## Стандартная иерархия файлов

Для того чтобы разделить код, вам нужен так называемый коллектор блупринтов, сами блупринты и бот, который может быть сгруппирован с коллектором. Самая простая иерархия:

```
* bot.py

* blueprints
- chat.py
- admin.py
```

### `bot.py`

Сначала разберем код файла `bot.py`, самый простой коллектор, который можно использовать - коллектор из коробки `load_blueprints_from_package`, он принимает только название пакеты из которого следует загружать блупринты

Для начала следует импортировать нужные объекты:

```python
from vkbottle import Bot, load_blueprints_from_package
```

Далее нужно создать самого бота:

```python
bot = Bot("token")
```

Теперь с помощью коллектора и бота можно сконструировать все блупринты:

```python
for bp in load_blueprints_from_package("blueprints"):
    bp.load(bot)
```

Осталось только запустить бота:

```python
bot.run_forever()
```

### `chat.py`

1. Добавим в auto_rules правило, которое будет следить чтобы все сообщения шли только из чата
2. Создадим правило и добавим его в auto_rules, которое будет получать информацию о чате и возвращать ее для всех хендлеров этого блупринта
3. Добавим несколько хендлеров

```python
from vkbottle.bot import Blueprint, Message, rules
from vkbottle_types.objects import MessagesConversation

class ChatInfoRule(rules.ABCRule[Message]):
    async def check(self, message: Message) -> dict:
        chats_info = await bp.api.messages.get_conversations_by_id(message.peer_id)
        return {"chat": chats_info.items[0]}

bp = Blueprint("for chat commands")
bp.labeler.vbml_ignore_case = True
bp.labeler.auto_rules = [rules.PeerRule(from_chat=True), ChatInfoRule()]

@bp.on.message(command="самобан")
async def kick(message: Message, chat: MessagesConversation):
    await bp.api.messages.remove_chat_user(message.chat_id, message.from_id)
    await message.answer(f"Участник самоустранился из {chat.chat_settings.title} по собственному желанию")

@bp.on.message(text="где я")
async def where_am_i(message: Message, chat: MessagesConversation):
    await message.answer(f"Вы в <<{chat.chat_settings.title}>>")
```

### `admin.py`

> Пусть команды из этого блупринта будут доступны только, например, создателю бота

1. Создадим проверку на id пользователя, написавшего сообщение
2. Добавим несколько хендлеров

<!-- todo сегодня не первое апреля, можно сделать пример с рассылкой -->

```python
from vkbottle.bot import Blueprint, Message, rules

bp = Blueprint("for admin commands")
bp.labeler.auto_rules = [rules.FromPeerRule(1)] # Допустим, вы являетесь Павлом Дуровым

@bp.on.message(command="halt")
async def halt(_):
    exit(0)
```

## Экзамплы по этой части туториала

* [blueprint](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/blueprint.py)
