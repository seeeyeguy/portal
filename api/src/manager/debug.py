"""
Debugpy integration module for remote debugging.

Starts a debugpy listener when ENABLE_DEBUGPY environment variable
is set to 'true'. This allows attaching a DAP-compatible debugger
(e.g., Neovim nvim-dap) to the running process.

Usage:

    Import and call `setup_debugpy()` early in the application
    lifecycle (e.g., in manage.py or settings.py).

    The default port for the API container is 5678.
"""

import logging
import os

LOGGER = logging.getLogger(__name__)


def setup_debugpy(port: int = 5678) -> None:
    """
    Start a debugpy listener if ENABLE_DEBUGPY is set to 'true'.

    Args:
        port: The port number to listen on. Default is 5678.
    """
    if os.environ.get("ENABLE_DEBUGPY", "false").lower() != "true":
        return

    # Prevent debugpy from starting on RQ nodes since they use
    # the debug-wrapper.sh script with their own ports.

    if os.environ.get("REDIS_RQ_NODE"):
        return

    try:
        import debugpy  # pylint: disable=import-outside-toplevel

        # Prevent multiple debugpy listeners in the same process
        # (e.g., Django runserver auto-reloader spawns a child).
        if not debugpy.is_client_connected():
            debugpy.listen(("0.0.0.0", port))
            LOGGER.info("debugpy listening on port %d", port)
    except Exception as exc:
        LOGGER.warning("Failed to start debugpy: %s", exc)
