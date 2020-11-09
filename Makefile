fix:
	black .
	autoflake --recursive --in-place --exclude=__init__.py,venv --remove-all-unused-imports --remove-duplicate-keys .

test:
	poetry run pytest --cov vkbottle tests
	poetry run mypy vkbottle
	poetry run flake8

publish:
	poetry build
	poetry config pypi-token.pypi ${PYPI_TOKEN}
	poetry publish
