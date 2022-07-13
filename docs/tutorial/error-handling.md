# Обработка ошибок

Иногда при запросах к api вконтакте возникают ошибки, для их обработки во фреймворке предусмотрено несколько инструментов

## try ... except VKAPIError

Для начала разъясним что такое `VKAPIError`, это подтип `CodeException`, особенность которого заключается в том, чтобы ошибка идентифицировалась в except и без указанного кода (`try except VKAPIError`) и при указании кода (`try except VKAPIError[code]`)

В `VKAPIError` есть два поля:

* `code` - код ошибки, int
* `description` - описание ошибки, str

Чтобы использовать `VKAPIError` нужно импортировать его:

```python
from vkbottle import VKAPIError
```

Теперь можно обернуть какой нибудь код с запросом к API:

```python
try:
    await api.wall.post()
except VKAPIError as e:
    print("Возникла ошибка", e.code)
```

При исполнении этого кода vk вернет ошибку, из-за того что не были переданы нужные параметры

## try ... except VKAPIError[code]

Кроме более общего способа для обработки всех ошибок vk в одном блоке except, вы можете воспользоваться более конкретным `VKAPIError[code]`

!!! info "Примечание"
    Список всех ошибок с их кодами вы можете найти [здесь](https://dev.vk.com/reference/errors)

Сделаем несколько блоков для демонстрации того, как первый и второй способ можно комбинировать

```python
try:
    await api.messages.send(peer_id=1, message="привет!", random_id=0)
except VKAPIError[902] as e:
    print("не могу отправить сообщение из-за настроек приватности")
except VKAPIError as e:
    print("не могу отправить:", e.error_description)
```

## Специфичные ошибки

Некоторые ошибки vk имеют дополнительные поля, которые могут понадобиться вам для их обработки:

* `CaptchaError`:
    * `sid` - идентификатор captcha, int
    * `img` - ссылка на изображение, str

## ErrorHandler

!!! info "Примечание"
    Инструмент будет рассматриваться конкретно с ботом, хоть это и отдельный объект, так как это - туториал - упрощенный вариант документации

    Техническая документация по хендлеру ошибок [здесь](../low-level/exception_handling/error-handler.md)

У `ErrorHandler` есть 4 метода:

* `register_error_handler` - декоратор, принимающий типы ошибок и асинхронную функцию-хендлер. Если возникнет одна из указанных ошибок (или её подтипа), исполнится указанный хендлер.
* `register_undefined_error_handler` - декоратор, принимающий тип ошибки и асинхронную функцию-хендлер. Если возникнет неизвестная ошибка, исполнится этот хендлер.
* `handle`, принимающий экземпляр ошибки. Передаёт ошибку в соответствующий хендлер, зарегистрированный с помощью вышеописанных декораторов. Если для данной ошибки нет хендлера, поднимает её.
* `catch` - декоратор. Ловит ошибки из декорированной функции и передаёт их методу `handle`.

```python
from vkbottle import Bot, VKAPIError

bot = Bot("token")


@bot.error_handler.register_error_handler(RuntimeError)
async def runtime_error_handler(e: RuntimeError):
    print("возникла ошибка runtime", e)


@bot.error_handler.register_error_handler(VKAPIError[902])
async def unable_to_write_handler(e: VKAPIError):
    print("человек не разрешил отправлять сообщения", e)
```

В примере создано 2 хендлера ошибок: для `RuntimeError` и конкретизированного `VKAPIError`

Также можно регистрировать хендлеры сразу для нескольких типов ошибок:

```python
from typing import Union

from vkbottle import Bot, VKAPIError

bot = Bot("token")


@bot.error_handler.register_error_handler(TypeError, ValueError)
async def type_or_value_error_handler(e: Union[TypeError, ValueError]):
    print("возникла ошибка type или value", e)


@bot.error_handler.register_error_handler(*VKAPIError[6, 9])
async def limit_reached_write_handler(e: VKAPIError):
    print("ой, слишком много запросов", e)
```

Ещё у `ErrorHandler` есть параметр `redirect_arguments: bool`, который позволяет передавать в хендлер аргументы из задекорированной с помощью `catch` функции. В связке с ботом позволяет передать в хендлер контекстные аргументы из правил и мидлварей.

## swear

!!! info "Примечание"
    Инструмент будет рассматриваться конкретно с ботом, хоть это и отдельный объект, так как это - туториал - упрощенный вариант документации

Краткий вариант хендлера ошибок одним декоратором, важно что swear может декорировать как синхронные, так и асинхронные функции

```python
from vkbottle import swear
```

В swear необходимо первым аргументом передать ошибку, которую он будет хендлить, например тот же `RuntimeError` и на выбор:

* `exception_handler=func` - если у вас есть хендлер которым вы будете хендлить ошибку и возвращать из него нужное значение для функции
* `just_return=True` - если вам нужно просто вернуть ошибку из функции
* `just_log=True` - если вам нужно логировать ошибку и вернуть из декорированной функции `None`

```python
from vkbottle import swear

@swear(RuntimeError, just_return=True)
def my_func():
    raise RuntimeError("error")

my_func() # RuntimeError("error")
```
