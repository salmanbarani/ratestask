test:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/unit /tests/integration /tests/e2e
