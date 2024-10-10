"""
`BI Portal` `Profile` controller module. Controllers utilize the
Django ORM to fetch records within the `Profile` table. `Profile`
offers additional information about a user.
"""

import logging

from users import models

LOGGER = logging.getLogger(__name__)


class Profile:
    """
    Container class for functions related to retrieving `Profile`
    records. `Profile` offers additional information about a user.
    """

    @staticmethod
    def fetch_profile(user: str) -> models.Profile:
        """
        Fetch the `Profile` instance for the given user.

        Accepts:
            * user (str): The related user's email for the profile
                we are fetching.

        Returns:
            * profile (models.Profile): The `Profile` instance for
                the given user.
        """

        LOGGER.info(f"Fetching Profile for user: {user}.")
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]
