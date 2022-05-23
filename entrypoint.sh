#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for database..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.2
    done

    echo "Database SQL started"
fi

flask db upgrade

exec "$@"