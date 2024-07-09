# PROJECT TITLE

## REQUIREMENTS

1. A PostgreSQL database (production)
2. Docker v26.1.0+
3. Docker Compose v2.26
4. .ssh/ in project root directory
5. SSL Certificates on host (production)
6. Encryption Key for `SECRET_KEY`
7. .env file with contents outlined in .env.example

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

-   Place project description here.

## DEPLOYMENT

### DEVELOPMENT

### PRODUCTION

### Contributors

-   Michael C. Mullings (michael.c.mullings@l3harris.com)
-   Luis Ruelas Lisboa (luis.ruelaslisboa@l3harris.com)
