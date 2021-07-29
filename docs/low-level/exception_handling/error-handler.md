# Error-Handler

Хендлер ошибок нужен для быстрой и простой высокоуровневой обработки любых типов исключений

Для того чтобы начать с ним работу потребуется создать его и зарегистрировать в него хендлеры исключений

```python
from vkbottle import ErrorHandler

async def exc_handler_runtime(e: RuntimeError):
    print("Oh no runtime error occurred:", e)

async def exc_handler_lookup(e: LookupError):
    print("Oh no lookup error occurred:", e)

error_handler = ErrorHandler(redirect_arguments=False) # Если redirect_arguments = True то все аргументы обернутой функции будут поступать и в хендлер исключения тоже
error_handler.register_error_handler(RuntimeError, exc_handler_runtime)
error_handler.register_error_handler(LookupError, exc_handler_lookup)
```

Еще вы можете добавить хендлер для ненайденных ошибок:

```python
async def exc_handler_undefined(e: BaseException):
    print("Oh no unknown error occurred", e)

error_handler.register_undefined_error_handler(exc_handler_undefined)
```

Если вы не хотите писать регистрацию после определения хендлера вы можете сделать это с помощью декоратора:

```python
@error_handler.register_error_handler(ZeroDivisionError)
async def exc_handler_zero_division(e: ZeroDivisionError):
    print("Oops i caught a ZeroDivisionError", e)

# from vkbottle import VKAPIError
@error_handler.register_error_handler(VKAPIError[6]) # Не забывайте про возможность пользоваться этой фишкой фабрики исключений
async def exc_handler_vk_api_6(e: VKAPIError):
    print("Oops i caught a VKAPIError with code 6:", e)

# С register_undefined_error_handler так тоже можно
```

Теперь чтобы error_handler сработал на вашей асинхронной функции добавьте к ней декоратор:

```python
@error_handler.wraps_error_handler()
async def main():
    raise LookupError("I ve lost my keys")
```

Запустите ее и оцените вывод:

```python
# from asyncio import run
run(main())
```

```text
Oh no lookup error occurred: I ve lost my keys
```
