.PHONY: fix
fix:
	uv run ruff check . --fix
	uv run ruff format .

.PHONY: test
test:
	ENV=test uv run pytest

.PHONY: check
check:
	uv run ruff check .
	uv run ruff format . --check
	uv run mypy . --strict
	make test
	rm coverage.svg
	uv run coverage-badge -o coverage.svg

.PHONY: run
run:
	docker compose up -d --build

.PHONY: stop
stop:
	docker compose down
