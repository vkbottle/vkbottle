# Formatting

Формирование форматированного текста осуществляется с помощью вспомогательного класса `Formatter`, который наследует класс `str` и имеет два перегруженных метода: `format`, `format_map`.

```python
from vkbottle.tools.formatting import Formatter
```

Доступные типы форматирования:

- bold — полужирный.
- italic – курсив.
- url — ссылка.
- underline — подчеркнутый.

!!! info "Примечание"
    Для типов форматирования специально реализованы такие же по названию функции, которые импортируются из модуля `vkbottle.tools.formatting`.

Метод `format` принимает `*args`, `**kwargs` и форматирует строку по специальным заменам, которые заключаются в `{}`.

Например:
```python
Formatter("Hi, {}.").format("Alex")  # Hi, Alex.
Formatter("Hi, {name}.").format(name="Maria")  # Hi, Maria.
```

Метод также поддерживает специальные идентификаторы:

- bold
- italic
- underline

Пример использования:
```python
Formatter("{:bold}, nice formatting!").format("Wow")  # Wow, nice formatting!
Formatter("{framefork:italic} has been around for over 5 years!").format(framework="vkbottle")  # vkbottle has been around for over 5 years!
```

Для того, чтобы объединить типы форматов, используется синтаксис объединения через символ `+`.
```python
Formatter("Very cool {:bold+italic} ^_^").format("bold-italic message")  # Very cool bold-italic message ^_^
```

Метод `format_map` работает так же, как и `format`, за исключением того, что метод принимает один аргумент типа `Mapping`, который передается в метод `format`.
```python
Formatter("My bestie is {bestie:underline}").format(bestie="telegrinder")  # My bestie is telegrinder
```

Объект `Formatter` имеет 2 свойства для того, чтобы получить форматирование в виде `json`:

- format_data — словарь `{"version": ..., "items": [...]}`.
- raw_format_data — сырой объект `format_data`.

!!! info "Примечание"
    `format_data` необходим для методов, которые могут работать с форматированным текстом, например: `messages.send`. Более подробно ознакомиться можно в [документации](https://dev.vk.com/ru/reference/objects/message#format_data) VK API.


Класс `Format` необходим для представления типа форматирования, таких как: `bold`, `italic` и т. д. Класс поддерживает оператор `+=`, конкатенацию строк и самих типов-форматов.
```python
from vkbottle.tools.formatting import Format
```

Пример использования функций-форматирования:

```python
bold("Hello, ") + italic("World!")  # Hello, World! ('Hello, ' is bold, 'World!' is italic)
"Hello, " + italic("World!")  # Hello, World! ('World!' is italic)
bold("Hello") + ", " + italic("World!")  # Hello, World! ('Hello' is bold, 'World!' is italic)
bold("vkbottle documentation:") + " " + url(italic("click me"), href="vkbottle.readthedocs.io/ru/latest")  # vkbottle documentation: click me ('click me' has an url)
```

`Format` имеет 2 метода для того, чтобы получить форматирование в виде `json`:

- as_data — словарь `{"version": ..., "items": [...]}`.
- as_raw_data — сырой объект `as_data`.

Пример использования с методом `BaseMessageMin.answer()`:

```python
await message.answer(Formatter("Hello, {:bold}!").format("World"))
await message.answer(underline(bold("Hello") + ", " + italic("World!")))
```
