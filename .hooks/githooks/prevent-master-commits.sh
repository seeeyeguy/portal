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

PROTECTED_BRANCHES=('master' 'staging' 'dev')
CURRENT_BRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

PROMPT=$(echo -e "$YELLOW[pre-commit] You're about to push $CURRENT_BRANCH, is that what you intended? [y|n]: $RESET")

if [[ $CURRENT_BRANCH == ${PROTECTED_BRANCHES[0]} || $CURRENT_BRANCH == ${PROTECTED_BRANCHES[1]} || $CURRENT_BRANCH == ${PROTECTED_BRANCHES[2]} ]]; then
    read -p "$PROMPT" -n 1 -r < /dev/tty
    echo 
    if echo $REPLY | grep -E '^[Yy]$' > /dev/null; then
        echo -e "$GREEN[pre-commit] Push to $CURRENT_BRANCH executed.$RESET"
        exit 0 # Push will execute.
    fi
    echo -e "$RED[pre-commit] Push to $CURRENT_BRANCH aborted.$RESET"
    exit 1 # Push will not execute.
else
    exit 0 # Push will execute.
fi