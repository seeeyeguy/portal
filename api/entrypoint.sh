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
    else
        # Collect all static files and place them in static root
        # to be served.
        python manage.py collectstatic --no-input
    fi

    # Apply migrations, ensuring to specify the target databases.
    python manage.py migrate auth 0012_alter_user_first_name_max_length --database=prt    
    python manage.py migrate program_review_tool --database=prt
    python manage.py migrate --database=default   

    python manage.py crontab add
    /apps/init.sh
fi

exec "$@"