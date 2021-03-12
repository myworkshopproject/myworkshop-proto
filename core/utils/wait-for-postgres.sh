#!/bin/sh
set -e
while ! nc -z $POSTGRES_HOST 5432; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done
echo "Postgres is up - continue"
exec "$@"
