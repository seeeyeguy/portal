"""
`BI Portal` `Favorite` controller module.

Controllers utilize the Django ORM to create, fetch, update, and delete
records within the `Favorite` table. A `Favorite` represents a preferred
`Resource` for a user.

"""

import logging
from typing import List, Dict

from django.db import transaction
from django.db.models import Count, Max, QuerySet
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from directory.models import Resource
from preferences import exceptions, models
from analytics import exceptions as analytics_exceptions

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
            user_record: User = User.objects.only("username").get(username__iexact=user)
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
            err_msg = f"User (username={user}) does not exist."
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
            user_record: User = User.objects.get(username__iexact=user)

            # Create a list of `Favorite` ids from `ranked_favorites`
            favorite_ids: List[int] = [favorite["id"] for favorite in ranked_favorites]

            # Create a list of ranks from `ranked_favorites`.
            favorite_ranks: List[int] = [
                favorite["rank"] for favorite in ranked_favorites
            ]

            # Query `Favorite` records for the user given.
            favorite_records: QuerySet[models.Favorite] = (
                models.Favorite.objects.filter(user=user_record)
            ).order_by("rank")

            # Get the number of existing `Favorite` records.
            favorites_count: int = favorite_records.count()

            # Verify the number of records queried match the number
            # of favorites to update, else raise an exception.
            if favorites_count != favorite_records.filter(id__in=favorite_ids).count():
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
                    f" do not exist for the User (username: {user})."
                )
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 404)

            # Verify ranks match the ones in the `Favorite` records.
            if (
                favorites_count
                != favorite_records.filter(rank__in=favorite_ranks).count()
            ):
                err_msg: str = (
                    f"Ranks given: {favorite_ranks}, do not match existing ranks."
                )
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 400)

            # Get the max rank of existing favorites and add 1
            max_rank: int = favorite_records.last().rank + 1  # type: ignore[union-attr,operator]

            # Construct map of `Favorite` instance ids with their corresponding
            # new rank.
            favorite_rank_map: dict = {}
            for ranked_favorite in ranked_favorites:
                favorite_rank_map[ranked_favorite["id"]] = ranked_favorite["rank"]

            with transaction.atomic():
                # Temporarily update the ranks of the existing
                # `Favorite` records.
                for favorite in favorite_records:
                    favorite.rank = max_rank
                    max_rank += 1
                models.Favorite.objects.bulk_update(favorite_records, ["rank"])

                # Update the `Favorite` records.
                for favorite in favorite_records:
                    favorite.rank = favorite_rank_map[favorite.id]
                models.Favorite.objects.bulk_update(favorite_records, ["rank"])

            return favorite_records
        except User.DoesNotExist as exc:
            err_msg: str = f"User (username={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc
        except (KeyError, IntegrityError) as exc:
            err_msg: str = "Invalid parameters given."
            LOGGER.error(f"{err_msg} {exc}")
            raise exceptions.PreferencesError(err_msg, 400) from exc

    @staticmethod
    def delete_favorite(favorite_id: int) -> int:
        """
        Delete the `Favorite` record with the given id.

        Accepts:
            * favorite_id (int): The id of the `Favorite` record being deleted.

        Returns:
            * rows_affected (int): Number of rows removed.
        """

        LOGGER.info(f"Deleting Favorite instance with id: {favorite_id}.")

        # Delete `Favorite` record.
        rows_affected, _ = models.Favorite.objects.filter(id=favorite_id).delete()
        return rows_affected

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
            user_record: User = User.objects.get(username__iexact=user)

            # Query `Favorite` records of active `Resource`s for the user
            # and order the results by rank (ascending).
            favorites: QuerySet[models.Favorite] = models.Favorite.objects.filter(
                user=user_record, resource__active=True
            ).order_by("rank")
            return favorites
        except User.DoesNotExist as exc:
            err_msg: str = f"User (username={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc

    @staticmethod
    def fetch_favorited_resources(
        user: str | None = None,
        top: int | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> List[Dict]:
        """
        Return resources that are favorited, with the total favorite count for each resource.

        Args:
            user (str, optional): username of the user
            top (int, optional): return the top N resources ordered by total favorite count (desc).
            page (int, optional): page number for pagination (1-indexed).
            limit (int, optional): number of resources per page.

        Returns:
            List[Dict]: Each dict contains:
                {
                    "resource": {
                        "name": str,
                        "url": str,
                        "active": bool,
                        "deleted": bool
                    },
                    "favorite_count": int
                }
        """
        try:
            LOGGER.info(
                "Fetching favorited resources user=%s, top=%s, page=%s, limit=%s",
                user,
                top,
                page,
                limit,
            )

            # Resolve user record if provided
            user_record: User | None = None
            if user:
                user_record = User.objects.get(username__iexact=user)

            # Build base queryset of active resources with favorites
            base_qs = (
                models.Favorite.objects.filter(resource__active=True)
                .values(
                    "resource__id",
                    "resource__name",
                    "resource__url",
                    "resource__active",
                    "resource__deleted",
                )
                .annotate(favorite_count=Count("id"))
                .order_by("-favorite_count", "resource__name")
            )

            # Restrict to resources favorited by the user if provided
            if user_record is not None:
                user_resource_ids = (
                    models.Favorite.objects.filter(user=user_record)
                    .values_list("resource_id", flat=True)
                    .distinct()
                )
                base_qs = base_qs.filter(resource__id__in=list(user_resource_ids))

            # Apply `top`
            if top is not None:
                if top <= 0:
                    raise analytics_exceptions.AnalyticsError(
                        "`top` must be positive.", 400
                    )
                base_qs = base_qs[:top]

            # Apply pagination
            if page is not None or limit is not None:
                if not (page and limit):
                    raise analytics_exceptions.AnalyticsError(
                        "`page` and `limit` must be provided together.", 400
                    )
                if page <= 0 or limit <= 0:
                    raise analytics_exceptions.AnalyticsError(
                        "`page` and `limit` must be positive integers.", 400
                    )
                offset = (page - 1) * limit
                base_qs = base_qs[offset : offset + limit]

            # Build compact response
            results: List[Dict] = []
            for row in base_qs:
                resource_obj = {
                    "name": row["resource__name"],
                    "url": row["resource__url"],
                    "active": row["resource__active"],
                    "deleted": row["resource__deleted"],
                }
                results.append(
                    {
                        "resource": resource_obj,
                        "favorite_count": row["favorite_count"],
                    }
                )

            return results

        except User.DoesNotExist as exc:
            err_msg = f"User (username={user}) does not exist."
            LOGGER.error(err_msg)
            raise analytics_exceptions.AnalyticsError(err_msg, 404) from exc
