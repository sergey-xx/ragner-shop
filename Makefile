COMPOSE_PROJECT_NAME_DEV=rg_dev
COMPOSE_PROJECT_NAME_PROD=rg_prod

COMPOSE_FILE_DEV = docker/docker-compose.dev.yaml
COMPOSE_FILE_PROD = docker/docker-compose.prod.yaml
ENV_FILE_DEV = .env.dev
ENV_FILE_PROD = .env.prod


DC_DEV=docker compose -f $(COMPOSE_FILE_DEV) -p $(COMPOSE_PROJECT_NAME_DEV) --env-file $(ENV_FILE_DEV)
DC_PROD=docker compose -f $(COMPOSE_FILE_PROD) -p $(COMPOSE_PROJECT_NAME_PROD) --env-file $(ENV_FILE_PROD)

.PHONY: help \
dev-build dev-up dev-down dev-stop dev-restart dev-logs dev-shell \
dev-makemigrations dev-migrate dev-superuser dev-static

# ====================================================================================

dev-build:
	$(DC_DEV) build

dev-up:
	$(DC_DEV) up -d

dev-down:
	$(DC_DEV) down $(args)

dev-stop:
	$(DC_DEV) stop

dev-restart:
	$(DC_DEV) restart $(s)

dev-logs:
	$(DC_DEV) logs -f $(s)

dev-shell:
	$(DC_DEV) exec $(s) sh

dev-makemigrations:
	$(DC_DEV) exec admin_panel python manage.py makemigrations $(args)

dev-migrate:
	$(DC_DEV) exec admin_panel python manage.py migrate

dev-superuser:
	$(DC_DEV) exec admin_panel python manage.py createsuperuser

dev-static:
	$(DC_DEV) exec admin_panel python manage.py collectstatic --noinput

dev-load-config:
	$(DC_DEV) exec admin_panel python manage.py load_config

dev-mock-chats:
	$(DC_DEV) exec admin_panel python manage.py mockchats

dev-mock-items:
	$(DC_DEV) exec admin_panel python manage.py mockitems

dev-mock-codes:
	$(DC_DEV) exec admin_panel python manage.py mockcodes

dev-panel-shell:
	$(DC_DEV) exec admin_panel sh
