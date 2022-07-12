# Handling-Handler

Хендлеры это конечная точка в обработке событий. Хендлеры могут быть блокирующими (если нашелся подходящий хендлер другие уже не проверяются и не выполняются) и не блокирующими (в таком случае количество выполняемых хендлеров не ограничено и зависит от того какие пройдут). По умолчанию все хендлеры являются блокирующими

Хендлеры помечаются (лейблируются) с помощью декораторов. За это отвечает `Labeler` high-level инстанс с которым вы работаете. Пример с ботом:

```python
from vkbottle.bot import Bot, Message

bot = Bot("token")

@bot.on.message()
async def any_message(message: Message):
    await message.answer("Привет я бот")

bot.run_forever()
```

## Хендлеры ботов

### message

Этот хендлер показан в примере выше

Хендлер на все сообщения (и из чата, и из личных сообщений)

### chat_message

Хендлер на сообщения из чатов

### private_message

Хендлер на сообщения из личных диалогов

!!! info "Примечание"
    Типы хендлеров выше не делают ничего необычного, просто оперируют предустановленным правилом `PeerRule`:

    * в `message` он не предустанавливается
    * в `chat_message` - `PeerRule(True)`
    * в `private_message` - `PeerRule(False)`

В качестве аргументов декоратор принимает инстансы правил (`ABCRule`), а в качестве `kwargs` он принимает значение из custom_rules (подробнее в [туториале](../../tutorial/rules.md)

!!! info "Примечание"
    Если правило вернуло словарь, то он будет распакован и передан в качестве аргументов в хендлер, если он принимает их:

    ```python
    # Кастомное правило MyRule возвращает словарь `{"some_key": "some_value"}`
    @bot.on.message(MyRule())
    async def some_key_handler(message: Message, some_key: str):
        await message.answer(f"some_key={some_value}")

    @bot.on.message(MyRule())
    async def regular_handler(message: Message):
        await message.answer("Этот хендлер не принимает аргумент 'some_key', поэтому он и не был передан")

    @bot.on.message(MyRule())
    async def kwargs_handler(message: Message, **kwargs):
        await message.answer(f"В хендлере переданы аргументы: {kwargs}")
        # В хендлере переданы аргументы: {"some_key": "some_value"}
    ```
