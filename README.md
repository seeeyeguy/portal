# PROJECT TITLE

## REQUIREMENTS

1. A PostgreSQL database (production)
2. Docker v26.1.0+
3. Docker Compose v2.26
4. Install system dependencies for pillow & pygraphviz libraries
5. .ssh/ in project root directory
6. SSL Certificates on host (production)
7. Encryption Key for `SECRET_KEY`
8. .env file with contents outlined in .env.example

## Dev Dependencies

1. Python 3.11+

## Installation

1. Ensure host satisfies requirements
2. Clone repository with `git clone`
3. Ensure required `.ssh` directory present in project root
4. Create python virtual environment with `python -m venv api/.venv`
5. Activate python virtual environment with `source api/.venv/bin/activate`
6. Install project python dependencies with `pip install -r requirements.dev.txt`
7. Create `.env` in project root with environment variables outlined in `.env.example`
8. Install githooks with `.hooks/install-hooks.sh`

## DESCRIPTION

This repo provides all the required infrastructure source files to deploy a fully featured Docker containerized Django backend application with
various features & services i.e.: websockets support, django-rq jobs, redis cache, Jupyter Notebook, LDAP support, SSO support,
githooks (for pre-push verification), pytest, pylint checker, mypy, Swagger (for development deployments only) and others.


## DEPLOYMENT

Once you have set all the required environment variables in your project's `.env`. You
can proceed to deploy your application by running the following commands:

1. Build the containers:  `docker compose build`
2. Run the containers: `docker compose up -d`
3. Optionally you can exectute 1 & 2 one line with: `docker compose up -d --build`

### DEVELOPMENT

* For the `development` deployment, ensure you set `BUILD` & `DOCKER_COMPOSE_API_BUILD_TARGET` to the correct development values:

    * `BUILD=development | demo`
    * `DOCKER_COMPOSE_API_BUILD_TARGET=wsgi-development | asgi-development`

* Proceed to deploy the application using the `demo.docker-compose.yml` or `docker-compose.yml` files
by running:

    * Using `demo.docker-compose.yml`.
        * `docker compose -f  demo.docker-compose.yml build`.
        * `docker compose -f  demo.docker-compose.yml up -d`.
    * Using the default `docker-compose.yml`.
        * `docker compose build`.
        * `docker compose up -d`.

### PRODUCTION

* For the `production` deployment, ensure you set the `BUILD` & `DOCKER_COMPOSE_API_BUILD_TARGET` to the correct production values:

    * `BUILD=production | staging`
    * `DOCKER_COMPOSE_API_BUILD_TARGET=wsgi-production | asgi-production`

* Proceed to deploy the application using the `production.docker-compose.yml` file by running:

    * `docker compose -f production.docker-compose.yml build`.
    * `docker compose -f production.docker-compose.yml up -d`.

### Contributors

-   Michael C. Mullings (michael.c.mullings@l3harris.com)
-   Luis Ruelas Lisboa (luis.ruelaslisboa@l3harris.com)
