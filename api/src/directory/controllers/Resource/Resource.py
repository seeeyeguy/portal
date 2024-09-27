"""
`BI Portal` `Resource` controller module. Controllers create,
fetch, search, update, and delete records within the `Resource`
table. `Resource` represents a link to an internal tool within
L3Harris technologies. `Resource` is the primary content served
by `BI Portal`.
"""

import logging
from typing import cast, List, Literal, TypedDict, Union

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Page, Paginator
from django.db.models import Count, Max, QuerySet

from directory import exceptions
from directory.controllers.Resource.search import utils
from directory.models import Resource
from request.models import Request

LOGGER = logging.getLogger(__name__)


# Default page length used when using
# pagination on the search.
DEFAULT_PAGE_LENGTH: int = 50

# Map of many-to-many `Resource` fields to
# query filter.
MANY_TO_MANY_FILTER_MAP: dict = {
    "functions": "subfunctions__function__id__in",
    "subfunctions": "subfunctions__id__in",
    "employee_levels": "employee_levels__id__in",
    "tags": "tags__id__in",
}


class SearchParams(TypedDict):
    """
    Type annotation for Resource.search controller function params.
    """

    name: str
    description: str
    functions: List[int]
    subfunctions: List[int]
    employee_levels: List[int]
    tags: List[int]
    download: Union[bool | None]
    structure: Union[Literal["default"] | Literal["functree"]]
    serialize: bool
    limit: Union[int | None]
    page: Union[int | None]


class ResourceSearch:
    """
    Container class for searching `Resource` records.
    """

    @staticmethod
    # pylint: disable=too-many-locals
    def search(params: SearchParams) -> Union[QuerySet[Resource], dict]:
        """
        Searches for `Resource`s that meet the search criteria given.

        Accepts:
            * params (SearchParams): The paramaters containing the search
                criteria.
        Returns:
            * resources (Union[QuerySet[Resource], dict]): A collection
                of `Resources` that meet the search criteria in the form
                of either a QuerySet[Resource] or a dictionary which contains
                the `Resource`s in structured form.
        """

        try:
            # Fetch `Resource`s that:
            #  1. Are active.
            #       - The url points to an active site.
            #       - The `Resource` is the most recent revision.
            #  2. Have a linked `Request` whose status is `APPROVED`.
            #       - That `Request` has transitioned through each
            #         stage in the request workflow, receiving all
            #         appropriate dispositions.
            resources: QuerySet[Resource] = Resource.objects.filter(
                active=True,
                requests__status=Request.RequestStatus.APPROVED,
            )

            # This query is for collecting the ids of the `Resource`s with
            # the highest revision_number for a each uid.
            resource_ids: QuerySet[Resource] = (
                resources.values("uid")
                .annotate(Max("id"), Max("revision_number"))
                .values_list("id__max", flat=True)
            )

            # Filter `resources` for entries with ids that are in
            # `resource_ids`.
            resources = resources.filter(id__in=resource_ids)

            # If `download` in `params` is not equal to `None`, filter
            # queryset for `Resource`s matching the `download`
            # value given.
            if params["download"] is not None:
                resources = resources.filter(download=params["download"])

            # Filter resources for those that match the `Function`, `SubFunction`,
            # `EmployeeLevel` and `Tag` ids given in `params`.
            for many_to_many_field, field_query in MANY_TO_MANY_FILTER_MAP.items():
                # pylint: disable=line-too-long
                param_m2m_ids_list: List[int] = params[many_to_many_field]  # type: ignore[literal-required]
                if param_m2m_ids_list:
                    resources = resources.filter(**{field_query: param_m2m_ids_list})

            # Get the `name` and `description` search terms from `params`.
            name_search_term: str = params["name"]
            description_search_term: str = params["description"]
            # If `name_search_term` or `description_search_term`
            # are non-empty, filter the `Resource`s to conform to the
            # search criteria.
            if name_search_term or description_search_term:
                # Use Postgres built-in search functionality to perform a
                # full-text search against the data in the database, similar
                # to a search engine, with the name and/or description provided.
                search_query: SearchQuery = SearchQuery(name_search_term) | SearchQuery(
                    description_search_term
                )
                search_vector: SearchVector = SearchVector("name", "description")
                resources = (
                    resources.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                        visits__count=Count("visits"),
                    )
                    .filter(search=search_query)
                    .order_by("-rank", "visits__count")
                )
            else:
                # Order the `Resource's by their visit count(descending).
                resources = resources.annotate(Count("visits")).order_by(
                    "-visits__count"
                )

            # If `limit` is given, then limit the results.
            resources = resources[: params["limit"]] if params["limit"] else resources

            # Get the page number from `params`.
            page_num: Union[int | None] = params["page"]
            if page_num:
                # Create a Paginator to paginate the collection
                # of `Resource`s.
                paginator: Paginator = Paginator(resources, DEFAULT_PAGE_LENGTH)

                # If `page` number supplied in the params is greater
                # than the number of available pages, then return an
                # empty `Resource` QueryList or dictonary depending on
                # search structure provided.
                if page_num > paginator.num_pages:
                    return (
                        Resource.objects.none()
                        if params["structure"] == utils.DEFAULT_STRUCTURE
                        else {}
                    )

                # Get the corresponding Page
                page: Page = paginator.page(page_num)

                # Assigning the page's `Resource` QueryList to
                # `resources`.
                resources = cast(QuerySet[Resource], page.object_list)

            # If the `structure` value given in `params` is
            # equal to FUNCTREE_STRUCTURE then proceed to
            # return the result of the util function that
            # structures the `Resource` data.
            if params["structure"] == utils.FUNCTREE_STRUCTURE:
                return utils.structure_resources(
                    resources=resources, serialize=params["serialize"]
                )
            return resources
        except KeyError as exc:
            error_msg = f"Missing parameter: `{exc}` from search paramters."
            LOGGER.error(error_msg)
            raise exceptions.DirectoryError(error_msg, status=400) from exc
        except TypeError as exc:
            LOGGER.error(exc)
            error_msg = "Incorrect value given for a search parameter."
            raise exceptions.DirectoryError(error_msg, status=400) from exc
