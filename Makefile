DC = docker-compose -f docker/docker-compose.yml

build:
	$(DC) build
	
up:
	$(DC) up -d

buildup:
	$(DC) up --build -d

down:
	$(DC) down -v

logs:
	$(DC) logs -f

ps:
	$(DC) ps

tests:
	$(DC) run --rm alembic pytest app --disable-warnings -v

lint:
	$ flake8 app --max-line-length=120 --exclude=alembic