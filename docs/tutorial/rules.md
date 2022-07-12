# Правила

Для того чтобы хендлер ловил только нужные сообщения/другие ивенты, нужны правила (rules, рулзы - устоявшаяся транслитерация в комьюнити вкботла), в вкботле существует множество рулзов прямо из коробки.

!!! warning "Внимание"
    Все встроенные рулзы работают только с объектом `Message`, для обработки сырых евентов нужно писать свою реализацию.

Есть несколько способов использования правил:

1. Импортировать их из `vkbottle.dispatch.rules.base` и использовать, инициализируя прямо в декораторе или в любой другой части кода:

    ```python
    from vkbottle.dispatch.rules.base import CommandRule
    from typing import Tuple

    @bot.on.message(CommandRule("say", ["!", "/"], 1))
    async def say_handler(message: Message, args: Tuple[str]):
        await message.answer(f"<<{args[0]}>>")
    ```

2. Использовать шорткаты, список с названиями можно найти [здесь](../high-level/routing/rules.md)

    ```python
    @bot.on.message(command=("say", 1))
    async def say_handler(message: Message, args: Tuple[str]):
        await message.answer(f"<<{args[0]}>>")
    ```

!!! info "Примечание"
    Некоторые правила принимают в качестве аргумента итерируемый объект.<br />
    Например, `CommandRule`, который принимает два аргумента: `command` и `args_count`, но при использовании шортката можно передавать их в кортеже:
    `python @bot.on.message(command=("help", 0))`

## Создание собственных правил

!!! info "Примечание"
    Правило - это класс соответствующий интерфейсу `ABCRule`, который должен реализовать лишь один асинхронный метод `check`, принимающий ивент и возвращающий `False` если проверка пройдена не была и `True` либо словарь с аргументами, которые будут распакованы в хендлер как непозиционные аргументы

### Создание правил напрямую

Чтобы создать правила импортируем `ABCRule` и имплементируем асинхронный метод `check`, еще стоит импортировать `Union` из `typing` для типизации вашего кода:

```python
from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class MyRule(ABCRule[Message]):
    async def check(self, event: Message) -> Union[dict, bool]:
        ...
```

Теперь стоит имплементировать логику правила `MyRule`, пусть оно будет просто проверять что длина сообщения меньше ста символов:

```python
return len(message.text) < 100
```

Вот что получилось:

!!! info "Примечание"
    Union в данном правиле не понадобился поэтому его допустимо опустить по стандартам mypy, в любом случае на сигнатуру это не повлияет

```python
from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class MyRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        return len(event.text) < 100
```

Теперь правило можно использовать как первым способом:

```python
@bot.on.message(MyRule())
```

Вторым способом рулзом `MyRule` в текущем состоянии воспользоваться не получится, из-за отсутствия каких-либо параметров правила, предлагается его кастомизировать с помощью метода `__init__`:

```python
# Новый вид правила
class MyRule(ABCRule[Message]):
    def __init__(self, lt: int = 100):
        self.lt = lt

    async def check(self, event: Message) -> bool:
        return len(event.text) < self.lt
```

Теперь, если предварительно (до объявления хендлеров) зарегистрировать правило в локальный лейблер

```python
bot.labeler.custom_rules["my_rule"] = MyRule
```

Его можно будет использовать и вторым способом:

```python
@bot.on.message(my_rule=50)
```

### Создание правил через правила-врапперы

!!! info "Примечание"
    Есть так называемые правила-врапперы, правила - которые исполняют какой-то код который получают как параметры

К правилам-врапперам из коробки можно отнести: `func`, шорткат для `FuncRule`; `coro` или `coroutine`, шорткат для `CoroutineRule`

`FuncRule` принимает в качестве аргумента функцию (которая может быть лямбдой). Созданное напрямую правило `MyRule` можно заменить вот так:

```python
@bot.on.message(func=lambda message: len(message.text) < 100)
```

## Экзамплы по этой части туториала

- [labeler-setup](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/labeler_setup.py)
- [rules-shortcuts](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/rules_shortcuts.py)
