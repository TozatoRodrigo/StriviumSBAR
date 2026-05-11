help:
	@echo "make help"
	@echo "make start"
	@echo "make stop"
	@echo "make restart"
	@echo "make test"
	@echo "make coverage"
	@echo "make format"
	@echo "make lint"
	@echo "make fix-lint"
start:
	@docker compose up -d

stop:
	@docker compose down

restart: stop start

migrate:
	@docker compose exec api poetry run alembic upgrade head

seed:
	@docker compose exec api poetry run python -m app.seed

test:
	@pytest

coverage:
	@pytest --cov=app --cov-report=html

format:
	@ruff format

lint:
	@ruff check

fix-lint:
	@ruff check --fix
