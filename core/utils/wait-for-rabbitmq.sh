#!/bin/sh
set -e
while ! nc -z $RABBITMQ_HOST 5672; do
    echo "RabbitMQ is unavailable - sleeping"
    sleep 1
done
echo "RabbitMQ is up - continue"
exec "$@"
