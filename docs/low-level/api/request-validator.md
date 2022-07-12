# Request-Validator

Валидации запросов к ВК нужны, например, для того, чтобы превращать списки чего-либо в строку с значениями через запятую как это требует вк

## Стандартные валидаторы ответов

### TranslateFriendlyTypesRequestValidator

Превращает стандартные типы питона в типы которые документирует вк:

* `list` -> `",".join(v)`
* `bool` -> `int(v)`
* `dict` -> `self.validate(v)`
* `BaseModel` -> `v.json()`

## Создание своего валидатора ответа

Пример с `request_validators` из `API`:

```python
from vkbottle import API, ABCRequestValidator

class SomeRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict) -> dict:
        # some stuff with request data
        return request

api = API("token")
api.request_validators.append(SomeRequestValidator())
```
