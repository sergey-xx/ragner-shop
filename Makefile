COMPOSE_PROJECT_NAME_DEV=rg_dev
COMPOSE_PROJECT_NAME_PROD=rg_prod

COMPOSE_FILE_DEV = docker/docker-compose.dev.yaml
COMPOSE_FILE_PROD = docker/docker-compose.prod.yaml
ENV_FILE_DEV = .env.dev
ENV_FILE_PROD = .env.prod


DC_DEV=docker compose -f $(COMPOSE_FILE_DEV) -p $(COMPOSE_PROJECT_NAME_DEV) --env-file $(ENV_FILE_DEV)
DC_PROD=docker compose -f $(COMPOSE_FILE_PROD) -p $(COMPOSE_PROJECT_NAME_PROD) --env-file $(ENV_FILE_PROD)

.PHONY: help \
build-dev up-dev down-dev stop-dev restart-dev logs-dev shell-dev \
makemigrations-dev migrate-dev superuser-dev static-dev

# ====================================================================================

build-dev:
	$(DC_DEV) build

up-dev:
	$(DC_DEV) up -d

down-dev:
	$(DC_DEV) down $(args)

stop-dev:
	$(DC_DEV) stop

restart-dev:
	$(DC_DEV) restart $(s)

logs-dev:
	$(DC_DEV) logs -f $(s)

shell-dev:
	$(DC_DEV) exec $(s) sh

makemigrations-dev:
	$(DC_DEV) exec admin_panel python manage.py makemigrations $(args)

migrate-dev:
	$(DC_DEV) exec admin_panel python manage.py migrate

superuser-dev:
	$(DC_DEV) exec admin_panel python manage.py createsuperuser

static-dev:
	$(DC_DEV) exec admin_panel python manage.py collectstatic --noinput

load-config-dev:
	$(DC_DEV) exec admin_panel python manage.py load_config

mock-chats-dev:
	$(DC_DEV) exec admin_panel python manage.py mockchats

mock-items-dev:
	$(DC_DEV) exec admin_panel python manage.py mockitems

mock-codes-dev:
	$(DC_DEV) exec admin_panel python manage.py mockcodes

panel-shell-dev:
	$(DC_DEV) exec admin_panel sh
