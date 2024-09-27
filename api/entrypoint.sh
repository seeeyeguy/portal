#!/usr/bin/env bash

PRODUCTION="production"
STAGING="staging"
DATABASE_HOST=database
DATABASE_PORT=5432

echo "Waiting for postgres..."

if [[ -n $BUILD  && $BUILD == $PRODUCTION ]]; then
    DATABASE_HOST=$POSTGRES_HOST
    DATABASE_PORT=$POSTGRES_PORT
fi

while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
done

echo "PostgreSQL started"

if [[ -z $REDIS_RQ_NODE && -z $ASGI_SERVER ]]; then
    if [[ $BUILD != $PRODUCTION && $BUILD != $STAGING ]]; then
        # Flush the database.
        python manage.py flush --no-input       
        
        # Deploy Jupyter Notebook.
        python manage.py shell_plus --notebook &> notebook.log &
        sleep 6
        sed -i "s/127.0.0.1/$SERVER_HOST/g" notebook.log 
    fi
    python manage.py migrate
    /apps/init.sh
fi

exec "$@"