# Рекомендации

Установка окружения через `python-poetry` (`make venv` или `poetry install`)

Рекомендовано использование `Makefile`

Для автоматического форматинга и линтинга лучше использовать `pre-commit` и `pre-push` хуки. Включить их можно через `make githooks` или `poetry run pre-commit install -t=pre-commit -t=pre-push`
