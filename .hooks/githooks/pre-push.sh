#!/usr/bin/env bash

# Reset
RESET='\e[0m'       # Text Reset

# Regular Colors
BLACK='\e[1;90m'        # Black
BLUE='\e[1;94m'         # Blue
CYAN='\e[1;96m'         # Cyan
GREEN='\e[1;92m'        # Green
PURPLE='\e[1;95m'       # Purple
RED='\e[1;91m'          # Red
WHITE='\e[1;97m'        # White
YELLOW='\e[1;93m'       # Yellow

PROJECT_BASE_DIR=$(git rev-parse --show-toplevel)
API_SRC_PATH="$PROJECT_BASE_DIR/api/src"

BLACK_VERSION=22.3.0
MYPY_VERSION=1.10.0
PYLINT_DJANGO_VERSION=2.5.5
PYLINT_VERSION=3.0.0

DJANGO_SYSTEM_CHECK_MESSAGE="System check identified no issues (0 silenced)."

# Ensure python .venv is activated.
echo -e "$GREEN[pre-push] Checking for Python venv...$RESET"
if [[ -z $VIRTUAL_ENV ]]; then
    echo -e "$RED[pre-push] Please activate your Python virtual environment with $YELLOW'source api/.venv/bin/activate'$RED.$RESET"
    exit 1
fi

# Ensure docker compose is installed/aliased.
echo -e "$GREEN[pre-push] Checking for Docker...$RESET"
if [[ ! $(which docker 2>/dev/null) ]]; then
    echo -e "$RED[pre-push] Please install docker and alias docker compose as$YELLOW dc='/usr/bin/docker compose'$RED.$RESET"
    exit 1
fi

# Ensure pylint is installed.
echo -e "$GREEN[pre-push] Checking for Pylint...$RESET"
if [[ ! $(pylint --version 2>/dev/null) ]]; then
    echo -e "$RED[pre-push] Pylint is required.$RESET"
    echo -e "$GREEN[pre-push] Installing$YELLOW pylint==$PYLINT_VERSION$GREEN.$RESET"
    pip install pylint==$PYLINT_VERSION
    if [[ $? != 0 ]]; then
        echo -e "$RED[pre-push] Installation failed. Please install$YELLOW pylint==$PYLINT_VERSION$RED manually.$RESET"
        exit 1
    fi
    pip install pylint_django==$PYLINT_DJANGO_VERSION
    if [[ $? != 0 ]]; then
        echo -e "$RED[pre-push] Installation failed. Please install$YELLOW pylint_django==$PYLINT_DJANGO_VERSION$RED manually.$RESET"
        exit 1
    fi
fi

# Ensure mypy is installed.
echo -e "$GREEN[pre-push] Checking for MyPy...$RESET"
if [[ ! $(mypy --version 2>/dev/null) ]]; then
    echo -e "$RED[pre-push] MyPy is required.$RESET"
    echo -e "$GREEN[pre-push] Installing$YELLOW mypy==$MYPY_VERSION$GREEN.$RESET"
    pip install mypy==$MYPY_VERSION
    if [[ $? != 0 ]]; then
        echo -e "$RED[pre-push] Installation failed. Please install$YELLOW mypy==$MYPY_VERSION$RED manually.$RESET"
        exit 1
    fi
fi

# Install black if needed and run formatter.
if [[ ! $(black --version 2>/dev/null) ]]; then
    echo -e "$RED[pre-push] Black Python Formatter is required.$RESET"
    echo -e "$GREEN[pre-push] Installing$YELLOW black==$BLACK_VERSION$GREEN.$RESET"
    pip install black==$BLACK_VERSION
    if [[ $? != 0 ]]; then
        echo -e "$RED[pre-push] Installation failed. Please install$YELLOW black==$BLACK_VERSION$RED manually.$RESET"
        exit 1
    fi
fi

# Format api/src with black formatter.
echo -e "$GREEN[pre-push] Formatting api/src...$RESET"
BLACK_FORMATTER_COMMAND=$(black $API_SRC_PATH --exclude /migrations)
if [[ $? != 0 ]]; then
    echo -e "$RED[pre-push] Black Formatter Failed. Please resolve issues.$RESET"
    exit 1
fi
echo -e "$GREEN[pre-push] Formatting Complete.$RESET"
echo -e "$YELLOW[pre-push] Ensure all formatting changes are committed and you are using black==$BLACK_VERSION as your default python formatter.$RESET"

# Run Django system check.
echo -e "$GREEN[pre-push] Running Django System Check...$RESET"
DOCKER_COMPOSE_DJANGO_SYSTEM_CHECK_COMMAND=$(docker compose exec api python manage.py check)
if [[ $? != 0 ]]; then
    echo -e "$RED[pre-push] Django System Check failed to run. Please resolve issues.$RESET"
    exit 1
fi
if [[ $DOCKER_COMPOSE_DJANGO_SYSTEM_CHECK_COMMAND != $DJANGO_SYSTEM_CHECK_MESSAGE ]]; then
    echo -e "$RED[pre-push] Django System Check Failed. Please resolve issues.$RESET"
    echo "$DOCKER_COMPOSE_DJANGO_SYSTEM_CHECK_COMMAND"
    exit 1
fi
echo -e "$GREEN[pre-push] Django System Check Passed.$RESET"

# Run Pytest.
echo -e "$GREEN[pre-push] Running API Test Suite...$RESET"
PYTEST_COMMAND=$(docker compose exec api pytest)
if [[ $? != 0 ]]; then
    echo -e "$RED[pre-push] Pytest failed to run. Please resolve issues.$RESET"
    exit 1
fi
PYTEST_CHECK=$(echo "$PYTEST_COMMAND" | tail -n 1 | grep failed)
if [[ -n "$PYTEST_CHECK" ]]; then
    echo -e "$RED[pre-push] API Test Suite Failed. Please fix tests.$RESET"
    echo "$PYTEST_COMMAND"
    exit 1
fi
echo -e "$GREEN[pre-push] API Test Suite Passed.$RESET"

# Run Pylint.
echo -e "$GREEN[pre-push] Running Pylint...$RESET"
PYLINT_REPORT_COMMAND=$(git diff --diff-filter=dr --name-only origin/dev HEAD | grep ".py$" | grep -v ".*migrations.*.py$" | grep -v "settings.py" | awk -vT=$PROJECT_BASE_DIR/ '{ print T$0 }' | xargs pylint --rcfile $PROJECT_BASE_DIR/api/.pylintrc --load-plugins pylint_django)
if [[ $? != 0 && $? != 123 ]]; then
    echo -e "$RED[pre-push] Pylint failed to run. Please resolve issues.$RESET"
    exit 1
fi
if [[ $PYLINT_REPORT_COMMAND == *"Your code has been rated at 10"* ]];
then
	echo -e "$GREEN*** Code rated at 10/10, PASS. ***$RESET"
else
	echo -e "$RED*** Code NOT rated at 10/10, FAIL. ***$RESET"
    echo "$PYLINT_REPORT_COMMAND"
    exit 1
fi

# Run MyPy.
echo -e "$GREEN[pre-push] Running MyPy...$RESET"
export PYTHONPATH=$API_SRC_PATH
MYPY_COMMAND=$(mypy $API_SRC_PATH --config=$PROJECT_BASE_DIR/api/mypy.ini)
if [[ $? != 0 && $? != 1 ]]; then
    echo -e "$RED[pre-push] MyPy failed to run. Please resolve issues.$RESET"
    exit 1
fi
if [[ $MYPY_COMMAND == "Success: no issues found"* ]];
then
	echo -e "$GREEN*** No issues found, PASS. ***$RESET"
else
	echo -e "$RED*** Issues found, FAIL. ***$RESET"
    echo "$MYPY_COMMAND"
    exit 1
fi