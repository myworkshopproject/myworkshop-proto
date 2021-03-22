include .env
default: help

.PHONY: dev
dev: ## Runs all services in development mode.
	docker-compose -p $(MYAPP_NAME)-dev \
	               up \
				   --build \
				   --remove-orphans \
				   --renew-anon-volumes

.PHONY: clean
clean: ## Cleans development environment (Docker containers and volumes).
	docker rm $(MYAPP_NAME)-dev_core_1
	docker rm $(MYAPP_NAME)-dev_reverse-proxy_1
	docker rm $(MYAPP_NAME)-dev_db_1
	docker volume rm $(MYAPP_NAME)-core-media-dev
	docker volume rm $(MYAPP_NAME)-db-data-dev

.PHONY: prod
prod: ## Runs all services in production mode, in detached mode.
	docker-compose -p $(MYAPP_NAME) \
	               -f docker-compose.yml \
				   up -d \
				   --build \
				   --remove-orphans \
				   --renew-anon-volumes

.PHONY: stop
stop: ## Stops all services running in production mode.
	docker-compose -p $(MYAPP_NAME) \
	               -f docker-compose.yml \
				   stop

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
