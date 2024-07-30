# Docker Compose

## Description:
Docker Compose is a tool that aids in defining and running multi-container applications. This document goes over some helpful commands.

## Documentation:
For more details on Docker Compose, please refer to the [official documentation](https://docs.docker.com/compose/).

## Commands:
 
* `build`: Builds or rebuilds your services.

    * Example: `docker-compose build`.
    * Note: By default `docker-compose.yml` is used as your configuration file. If you wish to use a different YAML file for a different deployment, i.e. `production.docker-compose.yml`, you can use the `-f` flag, i.e.: `docker compose -f production.docker-compose.yml build`.

* `up`: Creates and runs your containers.

    * Example: `docker-compose up`.
    * Note: As with the `build` command you can use a different YAML configuration file by using the `-f` flag, i.e.: `docker-compose -f production.docker-compose.yml up`.
    * Note: By default this command runs and shows the logs for all your defined containers in STDOUT. Using the `-d` flag (for "detached" mode) allows you to run your containers in the background, i.e.: `docker-compose up -d`.
    * Note: You can use the `--build` flag to build and start your servirces in one line, i.e.: `docker-compose up -d --build`.

* `down`: Stops and removes your containers & networks.

    * Example: `docker compose down`.

* `exec`: Executes a command in a running container.

    * Example: `docker compose exec <service_name> <command>`.
    * Example: Showing the applied migrations in the api container: `docker compose exec api python manage.py showmigrations`.

* `logs`: Shows the log output from containers.

    * Example: `docker compose logs`.
    * Note: By default this command shows the logs up to the moment this command is executed. If you wish to follow the logs, use the `-f` flag, i.e.: `docker compose logs -f`.
    * Note: You can specify the container for which you want to see the logs, i.e.: `docker compose logs -f <service_name>`.

* `ps`: Lists containers and their status.

    * Example: `docker compose ps`.



