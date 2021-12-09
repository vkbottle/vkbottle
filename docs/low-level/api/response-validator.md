# Response-Validator

Валидации ответов ВК нужны от случаев когда сервер по какой-то неизвестной причине возвращает html вместо json до правильно сформированной ошибки после запроса

## Стандартные валидаторы ответов

### JSONValidator

Парсит json из ответа с помощью самого правого json-парсера [из списка](../../modules.md). Если вернулся необрабатываемый тип (например `NoneType`), то отправляет запрос заново, пока не будет получен валидный ответ

### VKErrorValidator

Вызывает `VKAPIError` от `CodeException` при респонсе с ошибкой от вк

## Создание своего валидатора ответа

Пример с `response_validators` из `API`:

```python
from typing import Any, NoReturn, Union
from vkbottle import API, ABCResponseValidator


class SomeResponseValidator(ABCResponseValidator):
    async def validate(self, response: dict) -> Union[Any, NoReturn]:
        # some stuff with response
        return response

api = API("token")
api.response_validators.append(SomeResponseValidator())

```
