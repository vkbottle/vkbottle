# Keyboard

Клавиатуры в vkbottle можно генерировать очень просто.

Импортируйте `Keyboard`, `KeyboardButtonColor` и нужные вам `action` (например: `Text`, `OpenLink`, `Location`, `VKApps`, `Callback`)

Создайте объект клавиатуры:

```python
from vkbottle import Keyboard, KeyboardButtonColor, Text
keyboard = Keyboard(one_time=True, inline=False)  # О параметрах one_time и inline вы можете прочитать в документации к апи вконтакте
keyboard.add(Text("Кнопка 1"), color=KeyboardButtonColor.POSITIVE)  # Первая строка (ряд) добавляется автоматически
keyboard.row()  # Переходим на следующую строку 
keyboard.add(Text("Кнопка 2"))
keyboard.add(Text("Кнопка 3", payload={"command": 3}))
```

Теперь чтобы получить `json` для отправки клавиатуры в сообщении можно использовать метод объекта клавиатуры `get_json()`

Например:

```python
await message.answer(message="Смотри сколько кнопок!!", keyboard=keyboard.get_json())
```

Для клавиатуры доступен интерфейс билдера, поэтому весь код выше можно заменить этим:

```python
from vkbottle import Keyboard, KeyboardButtonColor, Text

# ...

await message.answer(
    message="Смотри сколько кнопок!!",
    keyboard=(
        Keyboard(one_time=True, inline=False)
        .add(Text("Кнопка 1"))
        .row()
        .add(Text("Кнопка 2"))
        .add(Text("Кнопка 3", payload={"command": 3}))
    ).get_json()
)
```

Для отправки пустой клавиатуры (чтобы удалить клавиатуру у пользователя) можете использовать `EMPTY_KEYBOARD` (нужно импортировать)
