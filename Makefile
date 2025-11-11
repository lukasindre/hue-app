.PHONY: fix
fix:
	uv run ruff check . --fix
	uv run ruff format .

.PHONY: run
run:
	docker compose up -d --build

.PHONY: stop
stop:
	docker compose down
