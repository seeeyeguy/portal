#!/usr/bin/env bash

PROJECT_BASE_DIR=$(git rev-parse --show-toplevel)
GIT_DIR="$PROJECT_BASE_DIR/.git"
HOOKS_DIR="$PROJECT_BASE_DIR/.hooks/githooks"

echo "Installing hooks..."
echo "$HOOKS_DIR"
# Create symlinks to our git hook scripts
echo -e "\t- Installing pre-push hook..."
ln -sf  $HOOKS_DIR/pre-push.sh $GIT_DIR/hooks/pre-push
echo -e "\t- Installing commit blocker..."
ln -sf $HOOKS_DIR/prevent-master-commits.sh $GIT_DIR/hooks/pre-commit

echo "Done!"