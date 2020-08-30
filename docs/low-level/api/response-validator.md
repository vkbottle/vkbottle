# Response-Validator

Валидации ответов ВК нужны от случаев когда сервер по какой-то неизвестной причине возвращает html вместо json до правильно сформированной ошибки после запроса

## Стандартные валидаторы ответов

### JSONValidator

Парсит json из ответа с помощью самого правого жсон-парсера [из списка](/docs/modules.md); Если вернулся необрабатываемый тип (например `NoneType`) то возбуждается `VKBottleError`

### VKErrorValidator

Вызывает `VKAPIError` от `CodeErrorFactory` при респонсе с ошибкой от вк

## Создание свего валидатора ответа

Пример с `response_validators` из `API`:

```python
from vkbottle import API, ABCResponseValidator
import typing


class SomeResponseValidator(ABCResponseValidator):
    async def validate(self, response: dict) -> typing.Union[typing.Any, typing.NoReturn]:
        # some stuff with response
        return response

api = API("token")
api.response_validators.append(SomeResponseValidator())
```