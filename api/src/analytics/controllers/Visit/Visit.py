"""
`BI Portal` `Visit` controller module. Controllers utilize the
Django ORM to create and fetch records within the `Visit` table.
`Visit` provides insights into users' behavior, particularly in
regards to the use of resources.
"""

import logging
from typing import List, Dict

from django.db.models import Count
from django.contrib.auth import models as AuthModels

from analytics import exceptions, models
from directory import models as DirectoryModels

LOGGER = logging.getLogger(__name__)


class Visit:
    """
    Container class for functions related to creating and
    retrieving `Visit` records. `Visit` provides insights
    into users' behavior, particularly in regards to the
    use of resources.
    """

    @staticmethod
    def create_visit(user: str, resource: int) -> models.Visit:
        """
        Create a `Visit` record in the database given a user and
        resource id.

        Accepts:
            * user (str): The user's email who visited a given resource.
            * resource (int): The id of the resource that is being visited.

        Returns:
            * visit (models.Visit): The newly created `Visit` record.
        """

        try:
            LOGGER.info(
                f"Creating Visit for User: {user} and Resource with id: {resource}."
            )

            # Fetch the `User` record.
            user_record: AuthModels.User = AuthModels.User.objects.get(
                email__iexact=user
            )

            # Fetch the `Resource` record.
            resource_record: DirectoryModels.Resource = (
                DirectoryModels.Resource.objects.get(id=resource, deleted=False)
            )

            # Create the `Visit` record.
            visit = models.Visit.objects.create(
                user=user_record, resource=resource_record
            )
            return visit
        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc

        except DirectoryModels.Resource.DoesNotExist as exc:
            err_msg = f"Resource (id={resource}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc

    @staticmethod
    def fetch_visited_resource(
        user: str | None = None,
        resource: int | None = None,
        top: int | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> List[Dict]:
        """
        Fetch aggregated `Visit` records based on the arguments passed to this
        controller. Results are grouped by resource and ordered by total visit
        count (descending).

        If `user`, `resource`, `top`, `page`, or `limit` are specified then
        a list of aggregated resource dicts will be returned matching the
        arguments. If no filters are provided, all active resources with visits
        will be returned.

        Accepts:
            * user (str | None): The username/email of the `User` whose visits
            should be considered.
            * resource (int | None): The id of the `Resource` to filter visits by.
            * top (int | None): Limit results to the top N resources ordered by
            total visit_count.
            * page (int | None): The page number of aggregated results to return
            (1-indexed).
            * limit (int | None): The number of aggregated results per page.

        Returns:
            List[Dict]: Each dict contains:
                {
                    "resource": {
                        "id": int,
                        "name": str,
                        "url": str,
                        "active": bool,
                        "deleted": bool
                    },
                    "visit_count": int
                }

        Raises:
            AnalyticsError: If parameters are invalid (e.g. non-positive `top`,
            `page`, or `limit`, or mixing `top` with `page/limit`).
            AnalyticsError (404): If the specified user or resource does not exist,
            or if no resources match the given parameters.
        """

        try:
            LOGGER.info(
                "Fetching visited resources user=%s, resource=%s, top=%s, page=%s, limit=%s",
                user,
                resource,
                top,
                page,
                limit,
            )

            # Resolve user record if provided
            user_record: AuthModels.User | None = None
            if user:
                try:
                    user_record = AuthModels.User.objects.get(username__iexact=user)
                except AuthModels.User.DoesNotExist:
                    return []

            # Build base queryset of active resources with visits
            base_qs = (
                models.Visit.objects.filter(resource__active=True)
                .values(
                    "resource__id",
                    "resource__name",
                    "resource__url",
                    "resource__active",
                    "resource__deleted",
                )
                .annotate(visit_count=Count("id"))
                .order_by("-visit_count", "resource__name")
            )

            # Restrict to user if provided
            if user_record is not None:
                base_qs = base_qs.filter(user=user_record)

            # Restrict to specific resource if provided
            if resource is not None:
                base_qs = base_qs.filter(resource__id=resource)

            # Apply `top`
            if top is not None:
                if top <= 0:
                    raise exceptions.AnalyticsError("`top` must be positive.", 400)
                base_qs = base_qs[:top]

            # Apply pagination
            if page is not None or limit is not None:
                if not (page and limit):
                    raise exceptions.AnalyticsError(
                        "`page` and `limit` must be provided together.", 400
                    )
                if page <= 0 or limit <= 0:
                    raise exceptions.AnalyticsError(
                        "`page` and `limit` must be positive integers.", 400
                    )
                offset = (page - 1) * limit
                base_qs = base_qs[offset : offset + limit]

            # Build compact response
            results: List[Dict] = []
            for row in base_qs:
                resource_obj = {
                    "id": row["resource__id"],
                    "name": row["resource__name"],
                    "url": row["resource__url"],
                    "active": row["resource__active"],
                    "deleted": row["resource__deleted"],
                }
                results.append(
                    {
                        "resource": resource_obj,
                        "visit_count": row["visit_count"],
                    }
                )

            return results

        except DirectoryModels.Resource.DoesNotExist as exc:
            err_msg = f"Resource (id={resource}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc
