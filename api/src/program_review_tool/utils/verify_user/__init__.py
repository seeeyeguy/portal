"""
`Program Review Tool` review utils module. Common functionality for the
`Program Review Tool` user verification, specifically it allows user authentication
 to work in a TEST environment.
"""

import logging

from django.contrib.auth import models as AuthModels
from manager.settings import ApplicationBuild, BUILD
from manager.services.ldap.provider.utils import fetch_authorized_employee

from program_review_tool import exceptions

LOGGER = logging.getLogger(__name__)


def verify_user(email: str) -> AuthModels.User:
    """
    Resolve email to a valid `AuthModels.User` instance.

    * Normalizes the address to the corporate domain.
    * Looks it up locally first.
    * In non‑test environments falls back to the LDAP helper.
    * Raises ``ProgramReviewToolError`` with a 404 if no user is found.

    Args:
        email: raw e‑mail supplied by the caller.

    Returns:
        The `User` instance that matches the e‑mail.

    """

    # Try local DB first.
    try:
        return AuthModels.User.objects.get(email__iexact=email)
    except AuthModels.User.DoesNotExist:
        # In non‑test environments attempt external verification.
        if BUILD != ApplicationBuild.TEST:
            verified = fetch_authorized_employee(email=email)
            if verified:
                return verified

        err_msg = f"User (email={email}) does not exist."
        LOGGER.error(err_msg)
        raise exceptions.ProgramReviewToolError(err_msg, 404)
