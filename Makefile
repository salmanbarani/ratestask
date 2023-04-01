help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build          Build docker images"
	@echo "  up             Run the docker containers"
	@echo "  down           To stop running containers"
	@echo "  show_logs      To see logs"
	@echo "  migrate        To sync your migrations to db"
	@echo "  makemigrations To make migration files"
	@echo "  collectstatic  To collectstatic files"
	@echo "  superuser      To create superuser"
	@echo "  down-v         To stop containers and remove volumes"
	@echo "  volume         To instpect volumes"
	@echo "  wookie-db      To to start psql from your terminal"
	@echo "  test           To run tests"
	@echo "  sh             To start shell from the projct container"
	@echo "  shell          To access api python console"
	@echo "  flake8         To check lintings"
	@echo "  black-check    Using black to for linting check"
	@echo "  black-diff     See linting differences before applying black"
	@echo "  black          to apply black linting"
	@echo "  isort-check    To check whether import sorts are correct"
	@echo "  isort-diff     To see sorts differences"
	@echo "  isort          To sort imports correctly"

build:
	docker compose -f docker-compose.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

show_logs:
	docker compose -f docker-compose.yml logs


test:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/unit /tests/integration /tests/e2e --disable-warnings
