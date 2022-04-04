#!/usr/bin/make

PROJECT_NAME = PerfomanceReview
USER = -u "$(shell id -u):$(shell id -g)"


help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[32m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

status: ## Информация о контейнерах
	@docker-compose ps

up: ## Запуск приложения
	UID=$(shell id -u) GID=$(shell id -g) docker-compose up -d

start: ## Запуск приложения
	@docker-compose start

stop: ## Остановка приложения
	@docker-compose stop

restart: ## Рестарт приложения
		@docker-compose restart

delete: ## Удаление приложения
	@docker-compose down --rmi all
