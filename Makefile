install: poetry.lock
	poetry install

run:
	poetry run python -m app
