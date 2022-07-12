# Клавиатуры и вложения

## Клавиатура

### Создание через `Keyboard`

```python
from vkbottle import Keyboard
```

`Keyboard` принимает параметры `one_time` и `inline` (их значение описано [здесь](https://vk.com/dev/bots_docs_3?f=4.2.%20Структура%20данных)).

Методы `Keyboard`:

- `add(action, color)` - добавляет кнопку к текущему ряду кнопок;
- `row()` - создаёт следующий ряд кнопок, переводит "курсор" на него;
- `get_json()` - преобразует клавиатуру в JSON-объект, который можно отправить в сообщении.

Создание клавиатуры использует `json.dumps` для преобразования в JSON-объект. Если ваша клавиатура статична, то вы можете избежать этой повторяющейся операции, создав её один раз, и используя уже "преобразованную" клавиатуру.

Примеры создания клавиатуры приведены [здесь](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/generate_keyboard.py), а отправить её можно так:

```python
keyboard = ...  # see examples above

@bot.on.message()
async def send_keyboard(message):
    await message.answer("Here is your keyboard!", keyboard=keyboard)
```

### Создание через `keyboard_gen` (устарело)

Устаревшая документация по устаревшему методу находится [здесь](https://github.com/vkbottle/vkbottle/blob/v2.0/docs/api.ru.md#генератор-keyboard_gen).

## Вложения

### Если у вас уже есть ссылка на вложение

Если у вас уже есть ссылка на вложение вида `"type{OWNER_ID}_{ITEM_ID}"` (например "photo-41629685_457239401"), то вы можете отправить её так:

```python
attachment = ... # see example above

@bot.on.message
async def send_attachment(message):
    await message.answer("See that attachment!", attachment=attachment)
```

### Если вы загружаете вложения динамически

Для того чтобы отправлять вложения, загруженные во время работы бота, нужны загрузчики. Прочитайте [документацию про загрузчики], и возвращайтесь сюда.

Пример отправки вложения, полученного из загрузчика:

```python
uploader = AnyUploader(bot.api)  # see uploaders types in "Uploaders documentation" above

@bot.on.message()
async def send_attachment(message):
    attachment = await uploader.upload("path/to/file")
    await message.answer("See that attachment!", attachment=attachment)
```

## Шаблоны

На данный момент ВКонтакте поддерживает только один вид шаблона — карусель. Документация по этому виду шаблона представлена [здесь](https://vk.com/dev/bot_docs_templates?f=5.%20Шаблоны%20сообщений).

Вы можете создать шаблон через vkbottle с помощью:

- `TemplateElement` - элемент шаблона. Названия полей соответствуют названиям полей в документации ВКонтакте.
- `template_gen` - создаёт шаблон из предоставленных элементов:

```python
from vkbottle.tools import template_gen, TemplateElement

my_template = template_gen(TemplateElement(...), TemplateElement(...), TemplateElement(...))
```

В этом примере `my_template` - уже готовый JSON-объект для отправки в сообщении. Вот пример его отправки:

```python
my_template = ...  # see example above

@bot.on.message()
async def send_template(message):
    await message.answer("Sending template...", template=my_template)
```

## Расширенные примеры по этой части

- [Создание клавиатуры](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/generate_keyboard.py)
- [Загрузка и отправка вложений](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/photo_upload_example.py)
