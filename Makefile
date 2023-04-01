help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build          Build docker images"
	@echo "  up             Run the docker containers"
	@echo "  down           To stop running containers"
	@echo "  show_logs      To see logs"
	@echo "  down-v         To stop containers and remove volumes"
	@echo "  test           To run tests"

build:
	docker compose -f docker-compose.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

down-v:
	docker compose -f docker-compose.yml down -v


show_logs:
	docker compose -f docker-compose.yml logs


test:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/unit /tests/integration /tests/e2e --disable-warnings
