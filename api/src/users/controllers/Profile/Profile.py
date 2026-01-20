"""
`BI Portal` `Profile` controller module. Controllers utilize the
Django ORM to fetch records within the `Profile` table. `Profile`
offers additional information about a user.
"""

import logging

from users import exceptions, models

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

        try:
            LOGGER.info(f"Fetching Profile for user: {user}.")

            # Query the profile for the given user.
            profile = models.Profile.objects.get(user__username__iexact=user)

            return profile
        except models.Profile.DoesNotExist as exc:
            err_msg = f"Profile for user (username={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.UsersError(err_msg, 404) from exc
