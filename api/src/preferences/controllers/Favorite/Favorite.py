"""
`BI Portal` `Favorite` controller module. Controllers utilize the
Django ORM to create, fetch, update, and delete records within
the `Favorite` table. `Favorite` represents a preferred `Resource`
for a user.
"""

import logging
from typing import List

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Max, QuerySet
from django.db.utils import IntegrityError

from directory.models import Resource
from preferences import exceptions, models

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

        try:
            # Fetch `User` record.
            user_record: User = User.objects.only("username").get(email__iexact=user)
            # Fetch `Resource` record.
            resource_record: Resource = Resource.objects.only("id").get(
                id=resource, active=True
            )

            # Ensure `Favorite` record doesn't already exist for the given `User`
            # and `Resource`.
            if models.Favorite.objects.filter(
                user_id=user_record.username, resource_id=resource_record.id
            ).exists():
                err_msg = f"Favorite already exists for User: {user} and Resource id: {resource}."
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 400)

            # Determine rank for the `Favorite` record being created.
            rank_aggregate: dict = models.Favorite.objects.filter(
                user_id=user_record.username
            ).aggregate(Max("rank"))
            rank: int = (
                rank_aggregate["rank__max"] + 1 if rank_aggregate["rank__max"] else 1
            )

            # Create `Favorite` record for the given `User` and `Resource`
            # with max rank.
            favorite_record: models.Favorite = models.Favorite.objects.create(
                user_id=user_record.username, resource_id=resource_record.id, rank=rank
            )

            return favorite_record

        except User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc
        except Resource.DoesNotExist as exc:
            err_msg = f"An active Resource (id={resource}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc

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
            * favorite_records (QuerySet[models.Favorite]): The `Favorite` records once
                they have been ranked for the given user.
        """

        try:
            log_msg: str = (
                # pylint: disable=line-too-long
                f"Ranking Favorites (ids: {[instance['id'] for instance in ranked_favorites]}) "
                f"for User: {user}."
            )
            LOGGER.info(log_msg)

            # Fetch `User` record.
            user_record: User = User.objects.get(email__iexact=user)

            # Create a list of `Favorite` ids from `ranked_favorites`
            favorite_ids: List[int] = [favorite["id"] for favorite in ranked_favorites]

            # Query `Favorite` records for the instance ids and user given.
            favorite_records: QuerySet[
                models.Favorite
            ] = models.Favorite.objects.filter(user=user_record, id__in=favorite_ids)

            # Verify the number of records queried match the number
            # of favorites to update, else raise an exception.
            if favorite_records.count() != len(ranked_favorites):
                user_favorite_record_ids: List[int] = list(
                    favorite_records.values_list("id", flat=True)
                )
                invalid_favorite_ids: List[int] = [
                    favorite_id
                    for favorite_id in favorite_ids
                    if favorite_id not in user_favorite_record_ids
                ]
                err_msg: str = (
                    f"Favorite ids given: {invalid_favorite_ids}"
                    f" do not exist for the User (email: {user})."
                )
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 404)

            # Update the `Favorite` records.
            with transaction.atomic():
                for favorite in ranked_favorites:
                    rank: int = favorite["rank"]
                    favorite_records.filter(id=favorite["id"]).update(rank=rank)

            return favorite_records
        except User.DoesNotExist as exc:
            err_msg: str = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc
        except (KeyError, IntegrityError) as exc:
            err_msg: str = "Invalid parameters given."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 400) from exc

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

        try:
            LOGGER.info(f"Fetching Favorites for user: {user}")

            # Fetch `User` record.
            user_record: User = User.objects.get(email__iexact=user)

            # Query `Favorite` records of active `Resource`s for the user
            # and order the results by rank (ascending).
            favorites: QuerySet[models.Favorite] = models.Favorite.objects.filter(
                user=user_record, resource__active=True
            ).order_by("rank")
            return favorites
        except User.DoesNotExist as exc:
            err_msg: str = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc
