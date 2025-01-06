"""
`BI Portal` `Favorite` controller module. Controllers utilize the
Django ORM to create, fetch, update, and delete records within
the `Favorite` table. `Favorite` represents a preferred `Resource`
for a user.
"""

import logging
from typing import List

from django.db.models import QuerySet

from preferences import models, exceptions

LOGGER = logging.getLogger(__name__)


class Favorite:
    """
    Container class for functions related to creating, updating,
    retrieving, and deleting `Favorite` records. `Favorite`
    represents a preferred `Resource` for a user.
    """

    @staticmethod
    def create_favorite(user: str, resource: int) -> models.Favorite:
        """
        Create a `Favorite` record in the database using the given
        user and resource id.

        Accepts:
            * user (str): The user that favorited the given resource.
            * resource (int): The id of the resource.

        Returns:
            * favorite (models.Favorite): The newly created `Favorite`
                record.
        """

        LOGGER.info(f"Creating Favorite for User: {user} and Resource: {resource}.")
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]

    @staticmethod
    def rank_favorites(
        user: str, ranked_favorites: List[dict]
    ) -> QuerySet[models.Favorite]:
        """
        Rank the `Favorite` for each record id in ranked_favorites for the given user.

        Accepts:
            * user (str): The user who is ranking their favorites.
            * ranked_favorites (List[dict]): List of dictionaries containing rankings
                for favorites in the form {"id": int, "rank": int}.

        Returns:
            * records (QuerySet[models.Favorite]): The `Favorite` records once
                they have been ranked for the given user.
        """

        log_msg = (
            # pylint: disable=line-too-long
            f"Ranking Favorites (ids: {[instance['id'] for instance in ranked_favorites]}) "
            f"for User: {user}."
        )
        LOGGER.info(log_msg)
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]

    @staticmethod
    def delete_favorite(favorite_id: int) -> int:
        """
        Delete the `Favorite` record with the given id.

        Accepts:
            * favorite_id (int): The id of the `Favorite` record being deleted.

        Returns:
            rows_affected (int): Number of rows removed.
        """

        try:
            LOGGER.info(f"Deleting Favorite instance with id: {favorite_id}.")

            # Fetch `Favorite` record to be deleted.
            favorite_record: models.Favorite = models.Favorite.objects.get(
                id=favorite_id
            )
            # Delete `Favorite` record.
            rows_affected, _ = favorite_record.delete()
            return rows_affected
        except models.Favorite.DoesNotExist as exc:
            err_msg: str = f"Favorite (id={favorite_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc

    @staticmethod
    def fetch_favorites(user: str) -> QuerySet[models.Favorite]:
        """
        Fetch all `Favorite` records for the given user.

        Accepts:
            * user (str): The user related to these favorited resources.

        Returns:
            favorites (QuerySet[models.Favorite]): All `Favorite`
                records for the given user.
        """

        LOGGER.info(f"Fetching Favorites for user: {user}")
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]
