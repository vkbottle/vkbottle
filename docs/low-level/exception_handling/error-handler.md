# Error-Handler

Хендлер ошибок нужен для быстрой и простой обработки любых типов исключений.

Для того, чтобы начать с ним работу, потребуется создать его и зарегистрировать в него хендлеры исключений:

```python
from vkbottle import ErrorHandler

error_handler = ErrorHandler(redirect_arguments=False, raise_exceptions=False)
# Если redirect_arguments = True, то все аргументы обернутой функции будут поступать и в хендлер исключения
# Если raise_exceptions = True, то все необработанные исключения будут выброшены (игнорируется, если есть обработчик для ненайденных ошибок)

@error_handler.register_error_handler(RuntimeError)
async def exc_handler_runtime(e: RuntimeError):
    print("Oh no runtime error occurred:", e)

@error_handler.register_error_handler(LookupError)
async def exc_handler_lookup(e: LookupError):
    print("Oh no lookup error occurred:", e)
```

Еще вы можете добавить хендлер для ненайденных ошибок:

```python
@error_handler.register_undefined_error_handler
async def exc_handler_undefined(e: Exception):
    print("Oh no unknown error occurred", e)
```

Теперь чтобы error_handler сработал на вашей асинхронной функции добавьте к ней декоратор:

```python
@error_handler.catch
async def main():
    raise LookupError("I ve lost my keys")
```

Запустите ее и оцените вывод:

```python
import asyncio

asyncio.run(main())
```

```text
Oh no lookup error occurred: I've lost my keys
```
