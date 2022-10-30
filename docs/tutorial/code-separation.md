# Разделение кода

!!! info "Примечание"
    Разделение кода - очень важная вещь для создания структуры проекта

Чтобы делать это, в vkbottle можно использовать составляющие фреймворка отдельно от `Bot`

Разделение кода, кроме того может быть очень грамотно использовано для создания локальных изменений в лейблере, например `auto_rules` поможет установить правила, которые будут накладываться на все хендлеры сообщений

!!! warning "Внимание"
    Правила в `auto_rules` распространяются только на хендлеры сообщений, для сырых евентов вам нужен `raw_event_auto_rules` и кастомные правила, работающие с ними

## Стандартная иерархия файлов

Для удобства разработки больших проектов, рекомендуется использовать подобную структуру файлов:

```text
/src/
├── handlers
│   ├── __init__.py
│   ├── admin.py
│   ├── chat.py
│   └── ping.py
├── bot.py
└── config.py
```

### `config.py`

Для начала создадим файл с конфигом, в котором будут храниться все глоабльные переменные, которые будут использоваться в разных частях проекта

```python
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler


api = API("token")
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

```

### `ping.py`

Теперь создадим файл `ping.py` в папке `handlers`, в котором будет простой хендлер, обрабатывающий сообщения с текстом `ping`

```python
from config import labeler

@labeler.message(text="ping")
async def ping_handler(message):
    await message.answer("pong")

```

### `chat.py`

В этом случае мы будем использовать `auto_rules`, чтобы автоматически добавлять правила к хендлерам,
поэтому создадим новый лейблер, который будет использоваться только в этом файле

1. Добавим в auto_rules правило, которое будет следить чтобы все сообщения шли только из чата
2. Создадим правило, которое будет получать информацию о чате и возвращать ее для всех хендлеров этого лейблера
3. Добавим несколько хендлеров

```python
from vkbottle.bot import BotLabeler, Message, rules
from vkbottle_types.objects import MessagesConversation

class ChatInfoRule(rules.ABCRule[Message]):
    async def check(self, message: Message) -> dict:
        chats_info = await message.ctx_api.messages.get_conversations_by_id(message.peer_id)
        return {"chat": chats_info.items[0]}


chat_labeler = BotLabeler()
chat_labeler.vbml_ignore_case = True
chat_labeler.auto_rules = [rules.PeerRule(from_chat=True), ChatInfoRule()]

@chat_labeler.message(command="самобан")
async def kick(message: Message, chat: MessagesConversation):
    await message.ctx_api.messages.remove_chat_user(message.chat_id, message.from_id)
    await message.answer(f"Участник самоустранился из {chat.chat_settings.title} по собственному желанию")

@chat_labeler.message(text="где я")
async def where_am_i(message: Message, chat: MessagesConversation):
    await message.answer(f"Вы в <<{chat.chat_settings.title}>>")
```

### `admin.py`

> Пусть эти команды будут доступны только, например, создателю бота

1. Создадим проверку на id пользователя, написавшего сообщение
2. Добавим несколько хендлеров

<!-- todo сегодня не первое апреля, можно сделать пример с рассылкой -->

```python
from vkbottle.bot import BotLabeler, Message, rules

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(1)] # Допустим, вы являетесь Павлом Дуровым

@admin_labeler.message(command="halt")
async def halt(_):
    exit(0)
```

### `__init__.py`

Теперь создадим файл `__init__.py` в папке `handlers`, в котором будем импортировать все лейблеры

```python
from .chat import chat_labeler
from .admin import admin_labeler
from .ping import labeler
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

__all__ = ("admin_labeler", "chat_labeler", "labeler")
```

### `bot.py`

Теперь мы можем создать файл `bot.py`, в котором будем создавать бота и регистрировать лейблеры

```python
from vkbottle import Bot
from config import api, state_dispenser, labeler
from handlers import chat_labeler, admin_labeler
```

> Так как мы создали файл `__init__.py` в папке `handlers`, интерпретатор выполнит код в `echo.py` и нам не нужно будет импортировать лейблер оттуда

Теперь нам нужно загрузить хендлеры в глобальный лейблер:

```python
labeler.load(chat_labeler)
labeler.load(admin_labeler)
```

Далее нужно создать самого бота и указать, какой лейблер использовать:

```python
bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)
```

Осталось только запустить бота:

```python
bot.run_forever()
```

## Экзамплы по этой части туториала

* [blueprint](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/blueprint.py)
