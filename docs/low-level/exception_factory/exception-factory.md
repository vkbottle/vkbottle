# Exception-Factory

Фреймворк заботится о том как вы будете хендлить исключения (не ошибки, а именно исключения, которые уже были выброшены; для того чтобы хендлить ошибки читайте соответствующую документацию)

## Использование

Стандартная фабрика для ошибок это `CodeErrorFactory`. Инициализированную фабрику можно импортировать под именем `VKAPIError`

### Вызов исключения и способы хендлинга с `CodeErrorFactory`

```python
CodeError = CodeErrorFactory() # VKAPIError

try:
    raise CodeError(code=1, error_description="Укажите error_description чтобы произвести выброс исключения")
except CodeError(1): # Ошибка с кодом 1
    print("Error with code 1 appeared")
except CodeError(): # Ошибка с любым кодом
    print("Error with unknown code appeared")
```
