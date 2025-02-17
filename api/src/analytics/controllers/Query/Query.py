"""
`BI Portal` `Query` controller module. Controllers utilize the
Django ORM to create and fetch records within the `Query` table.
`Query` provides insights into users' behavior, particularly in
regards to committed searches.
"""

import logging
from typing import cast, Union

from django.contrib.auth import models as AuthModels
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from analytics import exceptions, models
from directory.controllers.Resource.Resource import ResourceSearch, SearchParams
from directory.controllers.Resource.search.utils import DEFAULT_STRUCTURE
from directory.models.Resource import Resource

LOGGER = logging.getLogger(__name__)

DEFAULT_PAGE_LENGTH = 50


class Query:
    """
    Container class for functions related to creating and
    retrieving `Query` records. `Query` provides insights
    into users' behavior, particularly in regards to
    committed searches.
    """

    @staticmethod
    def create_query(user: str, search_term: str) -> models.Query:
        """
        Create a `Query` record in the database given a user and
        search term.

        Accepts:
            * user (str): The user's email who submitted the query.
            * search_term (str): A search term used when searching
                for resources.

        Returns:
            * query (models.Query): The newly created `Query` record.
        """

        try:
            LOGGER.info(
                f"Creating Query for User: {user} with search_term: {search_term}."
            )

            # Fetch the `User` record.
            user_record: AuthModels.User = AuthModels.User.objects.get(
                email__iexact=user
            )

            # Create the `Query` record.
            query: models.Query = models.Query.objects.create(
                user=user_record, search_term=search_term
            )

            search_params: SearchParams = {
                "name": search_term,
                "description": search_term,
                "functions": [],
                "subfunctions": [],
                "employee_levels": [],
                "tags": [],
                "download": None,
                "structure": DEFAULT_STRUCTURE,  # type: ignore
                "serialize": False,
                "limit": 5,
                "page": None,
            }
            # Search for `Resource`s based on search_term.
            resources: Union[
                QuerySet[Resource, Resource], dict
            ] = ResourceSearch.search(params=search_params)

            # Add `Resource`s to `Query`.
            query.resources.add(*resources)

            return query

        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc

    @staticmethod
    def fetch_query(
        record_id: int | None = None,
        user: str | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> Union[models.Query, QuerySet[models.Query]]:
        """
        Fetch all `Query` records based on the arguments passed to this
        controller. If page, limit, or user are specified then a QuerySet
        of `Query` records will be returned matching the arguments. If
        an id is specified then the associated `Query` record will be
        returned.

        Accepts:
            * record_id (int | None): The id of the `Query` record.
            * user (str): The user associated with the `Query` record(s).
            * page (int | None): The page of `Query` records to return.
            * limit (int | None): The limit of `Query` records to return.

        Returns:
            *queries (Union[models.Query, QuerySet[models.Query]]): The
                `Query` records based on the given arguments.
        """

        optional_args = f" with record_id: {record_id}" if record_id else ""
        optional_args = f" for User: {user}" if user != "" else optional_args
        optional_args = f" {optional_args} with page: {page}" if page else optional_args
        optional_args = (
            f"{optional_args}{' and ' if user or page else ' with '}limit: {limit}"
            if limit
            else optional_args
        )

        LOGGER.info(f"Fetching `Query`s{optional_args}.")

        try:
            # If a record id is given, along with a page
            # or limit then throw an invalid parameters error.
            if record_id and (page or limit):
                raise exceptions.AnalyticsError("Invalid parameters given.", 400)

            # If `record_id` is provided, return the record with the given id.
            if record_id:
                return models.Query.objects.get(id=record_id)

            queries: QuerySet[models.Query, models.Query] = models.Query.objects.all()

            # If `user` is provided, filter all queries by the given `user`.
            if user:
                user_record: AuthModels.User = AuthModels.User.objects.get(
                    email__iexact=user
                )
                queries: QuerySet[models.Query, models.Query] = queries.filter(
                    user=user_record
                )

            # If `limit` is given, then limit the number of results.
            if limit:
                queries = queries.order_by("-created")[:limit]

            # If `page` is provided, divide the queryset into pages according
            # to the default page length and return the given `page`.
            if page:
                # Create a Paginator to paginate the collection
                # of `Query`s.
                paginator: Paginator = Paginator(queries, DEFAULT_PAGE_LENGTH)

                # If `page` number supplied in the params is greater
                # than the number of available pages, then return an
                # empty `Query` QuerySet.
                if page > paginator.num_pages:
                    return models.Query.objects.none()

                # Get the corresponding Page.
                pages: Page = paginator.page(page)

                # Assigning the page's `Query` QuerySet to
                # `queries`.
                queries = cast(QuerySet[models.Query, models.Query], pages.object_list)

            return queries
        except models.Query.DoesNotExist as exc:
            err_msg = f"Query (id={record_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc
        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc
