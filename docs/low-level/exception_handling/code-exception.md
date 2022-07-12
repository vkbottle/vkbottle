# Code-Exception

Фреймворк заботится о том как вы будете хендлить исключения (не ошибки, а именно исключения, которые уже были выброшены; для того чтобы хендлить ошибки читайте соответствующую документацию)

## Использование

Базовый класс для исключений с кодом это `CodeException`.</br>
`CodeException` имеет generic-подобный синтаксис, код ошибки указывается в `[квадратных скобках]`.<br/>
Базовое Исключение для ошибок API можно импортировать под именем `VKAPIError`.

### Вызов исключения и способы хендлинга с `CodeException`

```python
class MyCodeError(CodeException):
    pass

try:
    raise MyCodeError[1]("Error description")
except MyCodeError[1]:
    print("Error with code 1 appeared")
except MyCodeError[2, 3]:
    print("Error with code 2 or 3 appeared")
except MyCodeError as e:  # Ошибка с любым кодом
    print(f"Error with code {e.code} appeared")
```
