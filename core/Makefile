default: help

.PHONY: venv
venv: ## Creates a virtual environment.
	python -m venv venv

.PHONY: install
install: ## Installs or updates dependencies.
	venv/bin/pip install --upgrade pip
	venv/bin/pip install pip-tools
	venv/bin/pip-compile
	venv/bin/pip-sync

.PHONY: migrations
migrations: ## Creates new migrations based on the changes detected to your models.
	venv/bin/python manage.py makemigrations

.PHONY: clean-migrations
clean-migrations: ## Remove all Django migrations.
	find . -path "*/migrations/*.py" -not -path "./venv*" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -not -path "./venv*" -delete

.PHONY: migrate
migrate: ## Synchronizes the database state with the current set of models and migrations.
	venv/bin/python manage.py migrate

.PHONY: populate-db
populate-db: ## Populates the database with initial values.
	venv/bin/python manage.py populate_db

.PHONY: collectstatic
collectstatic: ## Collects the static files into STATIC_ROOT.
	mkdir -p static
	venv/bin/python manage.py collectstatic --no-input --clear

.PHONY: clean-static
clean-static: ## Remove collected static files.
	rm -rf static

.PHONY: serve
serve: migrate populate-db ## Starts the production server.
	venv/bin/gunicorn myapp.wsgi:application \
	                  --bind 0.0.0.0:$(SERVER_PORT) \
	                  --workers 3 \
	                  --log-level=info

.PHONY: serve-dev
serve-dev: ## Starts the development server.
	venv/bin/python manage.py runserver 0.0.0.0:$(SERVER_PORT)

.PHONY: shell
shell: ## Starts the Python interactive interpreter.
	venv/bin/python manage.py shell

.PHONY: worker
worker: ## Starts a Celery worker.
	venv/bin/celery -A myapp worker --loglevel=INFO -n worker@%h

.PHONY: createsuperuser
createsuperuser: ## Creates a default superuser.
	venv/bin/python manage.py createsuperuser

.PHONY: generate_secret_key
generate_secret_key: ## Generate a Secret Key.
	venv/bin/python utils/secret_key.py

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
