#!/usr/bin/env bash

# Debug wrapper script for starting Python processes with debugpy
# Usage: debug-wrapper.sh <debug_port> <command> [args...]


DEBUG_PORT="${1}"
shift

if [[ -n "${ENABLE_DEBUGPY}" && "${ENABLE_DEBUGPY}" == "true" ]]; then
    echo "Starting with debugpy on port ${DEBUG_PORT}"
    # Remove --wait-for-client to let Django start immediately
    exec python -m debugpy --listen 0.0.0.0:${DEBUG_PORT} -m "$@"
else
    echo "Starting without debugpy (set ENABLE_DEBUGPY=true to enable)"
    exec python -m "$@"
fi
