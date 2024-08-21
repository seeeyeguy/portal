#!/usr/bin/env bash

PROJECT_BASE_DIR=$(git rev-parse --show-toplevel)
API_SRC_PATH="$PROJECT_BASE_DIR/api/src"

MANAGE_PY_PATH="$API_SRC_PATH/manage.py"
TEMPLATE_PATH="$API_SRC_PATH/manager/utils/apps/templates/app_template.tar.gz"


read -p "Enter app name: " app_name

if [ "${#app_name}" -gt 1 ]
    then python $MANAGE_PY_PATH startapp --template $TEMPLATE_PATH $app_name
fi