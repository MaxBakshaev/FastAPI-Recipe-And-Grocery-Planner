DC = docker-compose -f docker/docker-compose.yml

up:
	$(DC) up --build -d

down:
	$(DC) down -v

logs:
	$(DC) logs -f

ps:
	$(DC) ps