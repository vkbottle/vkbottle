# Response-Validator

Валидации ответов ВК нужны от случаев когда сервер по какой-то неизвестной причине возвращает html вместо json до правильно сформированной ошибки после запроса

## Стандартные валидаторы ответов

### JSONValidator

Парсит json из ответа с помощью самого правого json-парсера [из списка](../../modules.md). Если вернулся необрабатываемый тип (например `NoneType`), то запускает `Request Rescheduler`, пока не будет получен валидный ответ

### VKErrorValidator

Вызывает `VKAPIError` от `CodeException` при респонсе с ошибкой от вк

## Создание своего валидатора ответа

Пример с `response_validators` из `API` и `SomeRequestRescheduler` [отсюда](request-rescheduler.md)

```python
from typing import TYPE_CHECKING, Any, NoReturn, Union
from vkbottle import API, ABCResponseValidator
from .request_rescheduler import SomeRequestRescheduler

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

class SomeResponseValidator(ABCResponseValidator):
    async def validate(
        self,
        method: str,
        data: dict,
        response: Any,
        ctx_api: Union["ABCAPI", "API"],
    ) -> Union[Any, NoReturn]:
        if "error" not in response:
            return response
        if ctx_api.ignore_errors:
            return None
        if response["error"]["error_code"] != 6:
            return response
        # Обрабатываем ошибку 6, которая возникает при слишком частых запросах
        return await SomeRequestRescheduler().reschedule(
            ctx_api, method, data, response
        )

api = API("token")
# Этот валидатор должен идти после JSONResponseValidator,
# но раньше VKAPIErrorResponseValidator, чтобы он не обработал эту ошибку
api.response_validators.insert(1, SomeResponseValidator())

```
