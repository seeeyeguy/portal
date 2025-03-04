"""
`BI Portal` `Resource` controller module. Controllers create,
fetch, search, update, and delete records within the `Resource`
table. `Resource` represents a link to an internal tool within
L3Harris technologies. `Resource` is the primary content served
by `BI Portal`.
"""

# pylint: disable=wrong-import-order
import logging
import os
import requests
from PIL import Image
from typing import cast, List, Literal, Tuple, TypedDict, Union
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.paginator import Page, Paginator
from django.db.models import Count, Max, Q, QuerySet

from directory import exceptions
from directory.controllers.Resource.search import utils
from directory.models import EmployeeLevel, Resource as ResourceModel, SubFunction, Tag
from directory.utils import validate_url
from request.models import Request, Stage, Transition

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

RESOURCE_DESCRIPTION_MIN_CHAR_LENGTH = 30


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
    download: Union[bool, None]
    structure: Union[Literal["default"], Literal["functree"]]
    serialize: bool
    limit: Union[int, None]
    page: Union[int, None]


class BaseResourceParams(TypedDict):
    """
    Base type annotation used by create and update Resource
    controller function params.
    """

    name: str
    description: str
    url: str
    thumbnail: Image.Image
    employee_levels: List[int]
    subfunctions: List[int]
    tags: List[int]
    type: str
    download: bool


class CreateResourceParams(BaseResourceParams):
    """
    Type annotation for create Resource controller
    function params.
    """

    previous_revision: int | None
    uid: str


class UpdateResourceParams(BaseResourceParams):
    """
    Type annotation for update Resource controller
    function params.
    """

    resource_id: int


class Resource:
    """
    Container class for functions related to creating, updating, and
    retrieving `Resource` records. `Resource` represents a link to an
    internal tool within L3Harris technologies. `Resource` is the primary
    content served by `BI Portal`.
    """

    @staticmethod
    def create_resource(params: CreateResourceParams) -> ResourceModel:
        """
        Create a `Resource` record with the given params.

        Accepts:
            * params (CreateResourceParams): The parameters used to create
                a `Resource` record.

        Returns:
            * resource (ResourceModel): The `Resource` record created.
        """

        try:
            LOGGER.info(
                f"Creating Resource with uid: {params['uid']}, name: {params['name']}, "
                f"description: {params['description']}, previous revision: "
                f"{params['previous_revision']}, url: {params['url']}, employee levels: "
                f"{params['employee_levels']}, subfunctions: {params['subfunctions']}, "
                f"tags: {params['tags']}, type: {params['type']}, and download: "
                f"{params['download']}."
            )

            previous_revision: Union[ResourceModel, None] = (
                ResourceModel.objects.get(id=params["previous_revision"])
                if params["previous_revision"]
                else None
            )
            # Ensure new revision being created has the same uid as the previous revision.
            if previous_revision and (
                not params["uid"] or previous_revision.uid != params["uid"]
            ):
                err_msg = (
                    f"Resource (uid={params['uid']}) must match its previous revision."
                )
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, status=400)

            # Ensure a pending `Request` doesn't already exist for a `Resource` with
            # the given uid.
            if (
                previous_revision
                and ResourceModel.objects.filter(
                    uid=previous_revision.uid,
                    requests__status=Request.RequestStatus.PENDING,
                ).exists()
            ):
                err_msg = f"Resource (uid={params['uid']}) has a pending draft."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, status=400)

            resources_with_name: QuerySet[ResourceModel] = ResourceModel.objects.filter(
                Q(
                    name__iexact=params["name"],
                    active=True,
                    requests__status=Request.RequestStatus.APPROVED,
                )
                | Q(
                    name__iexact=params["name"],
                    requests__status=Request.RequestStatus.PENDING,
                )
            )
            # Ensure a `Resource` doesn't already exist with the given name.
            if resources_with_name.exclude(uid=params["uid"]).exists():
                err_msg = f"Resource (name={params['name']}) already exists."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, status=400)

            if (
                not params["description"]
                or len(params["description"]) < RESOURCE_DESCRIPTION_MIN_CHAR_LENGTH
            ):
                err_msg = (
                    "Please provide a more detailed description for this resource."
                )
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, status=400)

            validate_url(params["url"])

            if not params["employee_levels"]:
                err_msg = "Resource must be associated with at least one EmployeeLevel."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Fetch `EmployeeLevel` records.
            employee_level_records: QuerySet[
                EmployeeLevel
            ] = EmployeeLevel.objects.filter(id__in=params["employee_levels"])
            if employee_level_records.count() != len(set(params["employee_levels"])):
                err_msg = f"Some EmployeeLevels (ids={params['employee_levels']}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 404)

            if not params["subfunctions"]:
                err_msg = "Resource must be associated with at least one SubFunction."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Fetch `SubFunction` records.
            subfunction_records: QuerySet[SubFunction] = SubFunction.objects.filter(
                id__in=params["subfunctions"]
            )
            if subfunction_records.count() != len(set(params["subfunctions"])):
                err_msg = (
                    f"Some SubFunctions (ids={params['subfunctions']}) do not exist."
                )
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 404)

            # Fetch `Tag` records.
            tag_records: QuerySet[Tag] = Tag.objects.filter(id__in=params["tags"])
            if tag_records.count() != len(set(params["tags"])):
                err_msg = f"Some Tags (ids={params['tags']}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 404)

            resource: ResourceModel = ResourceModel.objects.create(
                uid=params["uid"] if previous_revision else uuid4(),
                previous_revision=previous_revision,
                revision_number=None,
                name=params["name"],
                description=params["description"],
                url=params["url"],
                thumbnail=params["thumbnail"],
                type=params["type"].lower(),
                download=params["download"],
                active=False,
            )

            # Add `EmployeeLevel`s, `SubFunction`s, and `Tag`s.
            resource.employee_levels.add(*employee_level_records)
            resource.subfunctions.add(*subfunction_records)
            resource.tags.add(*tag_records)

            return resource
        except ResourceModel.DoesNotExist as exc:
            err_msg = f"Resource (id={params['previous_revision']}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, status=404) from exc
        except ValidationError as exc:
            err_msg = f"URL({params['url']}) is malformed."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, status=400) from exc
        except requests.HTTPError as exc:
            err_msg = f"URL({params['url']}) is not reachable."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, status=404) from exc

    @staticmethod
    def update_resource(params: UpdateResourceParams) -> Tuple[ResourceModel, int]:
        """
        Update a `Resource` record for the given id with the given params.

        Accepts:
            * params (UpdateResourceParams): The parameters used to update
                a `Resource` record.

        Returns:
            * resource (ResourceModel): The updated `Resource` record.
            * rows_affected (int): The number of `Resource` records updated.
        """

        try:
            LOGGER.info(
                f"Updating Resource with id: {params['resource_id']}, name: "
                f"{params['name']}, description: {params['description']}, url: "
                f"{params['url']}, employee levels: {params['employee_levels']}, "
                f"subfunctions: {params['subfunctions']}, tags: {params['tags']}, "
                f"type: {params['type']}, and download: {params['download']}."
            )

            # Create a new non-typed dict from the `params` in order
            # to use `.pop()` method without warnings.
            new_params: dict = {**params}

            # Fetch the `Resource` record.
            resource: ResourceModel = ResourceModel.objects.get(
                id=new_params.pop("resource_id")
            )

            # Verify DRAFT status for `Resource` with shared
            # uid.
            if (
                ResourceModel.objects.filter(
                    uid=resource.uid, requests__status=Request.RequestStatus.PENDING
                )
                .exclude(id=resource.id)
                .exists()
            ):
                err_msg = f"Resource (uid={resource.uid}) has a pending draft."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Fetch related `Transition`(s) for target
            # `Resource` to update.
            transitions_query = Transition.objects.filter(
                request__resource=resource
            ).prefetch_related("stage")

            # Verify there are existing `Transition`s for
            # the target `Resource` and that the latest one
            # is for draft status.
            if (
                not transitions_query.exists()
                or transitions_query.order_by("-created").first().stage.level  # type: ignore[union-attr]
                != Stage.StageLevels.DRAFT
            ):
                err_msg = f"Resource (id={resource.id}) not in draft status."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            resources_with_name: QuerySet[ResourceModel] = ResourceModel.objects.filter(
                Q(
                    name__iexact=params["name"],
                    active=True,
                    requests__status=Request.RequestStatus.APPROVED,
                )
                | Q(
                    name__iexact=params["name"],
                    requests__status=Request.RequestStatus.PENDING,
                )
            )
            # Ensure a `Resource` doesn't already exist with the given name.
            if resources_with_name.exclude(uid=resource.uid).exists():
                err_msg = f"Resource (name={params['name']}) already exists."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, status=400)

            # Verify a `description` was given and of appropriate length.
            if (
                not params["description"]
                or len(params["description"]) < RESOURCE_DESCRIPTION_MIN_CHAR_LENGTH
            ):
                err_msg = (
                    "Please provide a more detailed description for this resource."
                )
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, status=400)

            # Validate `url`.
            validate_url(params["url"])

            employee_levels: List[int] = new_params.pop("employee_levels")
            subfunctions: List[int] = new_params.pop("subfunctions")
            tags: List[int] = new_params.pop("tags")

            # Verify `EmployeeLevel` ids were given.
            if not employee_levels:
                err_msg = "Resource must be associated with at least one EmployeeLevel."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Fetch `EmployeeLevel` records.
            employee_level_records: QuerySet[
                EmployeeLevel
            ] = EmployeeLevel.objects.filter(id__in=employee_levels)
            if employee_level_records.count() != len(employee_levels):
                err_msg = f"Some EmployeeLevels (ids={employee_levels}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 404)

            # Verify `SubFunction` ids were given.
            if not subfunctions:
                err_msg = "Resource must be associated with at least one SubFunction."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Fetch `SubFunction` records.
            subfunction_records: QuerySet[SubFunction] = SubFunction.objects.filter(
                id__in=subfunctions
            )
            if subfunction_records.count() != len(subfunctions):
                err_msg = f"Some SubFunctions (ids={subfunctions}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 404)

            # Fetch `Tag` records.
            tag_records: QuerySet[Tag] = Tag.objects.filter(id__in=tags)
            if tag_records.count() != len(tags):
                err_msg = f"Some Tags (ids={tags}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 404)

            # Get the thumbnail.
            thumbnail = new_params.pop("thumbnail")
            # Verify a thumbnail was given.
            if thumbnail:
                # If an existing thumbnail exists,
                # proceed to delete it.
                if resource.thumbnail:
                    try:
                        LOGGER.info(
                            "Deleting existing Resource (id=%s) thumbnail: %s",
                            resource.id,
                            resource.thumbnail.name,
                        )
                        os.remove(resource.thumbnail.path)
                    except FileNotFoundError:
                        pass

                # Update thumbnail.
                resource.thumbnail = thumbnail
                resource.save()

            rows_affected: int = ResourceModel.objects.filter(id=resource.id).update(
                **new_params
            )

            # Set `Function`s, `EmployeeLevel`s, and `Tag`s.
            resource.subfunctions.set(subfunction_records)
            resource.employee_levels.set(employee_level_records)
            resource.tags.set(tag_records)

            resource.refresh_from_db()

            return resource, rows_affected
        except KeyError as exc:
            error_msg = f"Missing parameter: `{exc}` from update parameters."
            LOGGER.error(error_msg)
            raise exceptions.DirectoryError(error_msg, status=400) from exc
        except ResourceModel.DoesNotExist as exc:
            err_msg = f"Resource (id={params['resource_id']}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc
        except ValidationError as exc:
            err_msg = f"URL({params['url']}) is malformed."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, status=400) from exc
        except requests.HTTPError as exc:
            err_msg = f"URL({params['url']}) is not reachable."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, status=404) from exc

    @staticmethod
    def fetch_resources(
        resource_id: int | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> Union[ResourceModel, QuerySet[ResourceModel]]:
        """
        Fetch a `Resource` record from the database with the given
        id or if no id is specified return all `Resource` records.
        If page is specified, return that page of records. If
        limit is specified, return up to `limit` number of records.

        Accepts:
            * resource_id (int | None): Optional parameter to either return a
                single `Resource` record with the specified id or all
                `Resource` records in the database.
            * page (int | None): The page of `Resource` records to return.
            * limit (int | None): The limit of `Resource` records to return.

        Returns:
            * resources (Union[ResourceModel, QuerySet[ResourceModel]]):
                Either one `Resource` instance with the specified id
                or a QuerySet of all `Resource` instances in accordance with
                the page and limit.
        """

        try:
            optional_args = f" with id: {resource_id}" if resource_id else "s"
            optional_args = (
                f"{optional_args} with page: {page}" if page else optional_args
            )
            optional_args = (
                f"{optional_args}{' and ' if page else ' with '}limit: {limit}"
                if limit
                else optional_args
            )
            LOGGER.info(f"Fetching Resource{optional_args}.")

            # If resource id is given, along with a page
            # or limit then throw an invalid parameters error.
            if resource_id and (page or limit):
                raise exceptions.DirectoryError("Invalid parameters given.", 400)

            # If a resource id is given, fetch the corresponding `Resource` record.
            if resource_id:
                return ResourceModel.objects.get(id=resource_id)

            resources = ResourceModel.objects.all()

            # If `limit` is given, then limit the `Resource` records.
            resources = resources[:limit] if limit else resources

            if page:
                # Create a Paginator to paginate the collection
                # of `Resource`s.
                # pylint: disable=line-too-long
                paginator: Paginator = Paginator(resources, DEFAULT_PAGE_LENGTH)

                # If `page` number supplied in the params is greater
                # than the number of available pages, then return an
                # empty `Resource` Queryset.
                if page > paginator.num_pages:
                    return ResourceModel.objects.none()

                # Get the corresponding Page.
                resource_page: Page = paginator.page(page)

                # Assign the page's `Resource` QuerySet to
                # `resources`.
                resources = cast(QuerySet[ResourceModel], resource_page.object_list)

            return resources

        except ResourceModel.DoesNotExist as exc:
            err_msg = f"Resource (id={resource_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc


class ResourceSearch:
    """
    Container class for searching `Resource` records.
    """

    @staticmethod
    # pylint: disable=too-many-locals
    def search(
        params: SearchParams,
    ) -> Union[QuerySet[ResourceModel, ResourceModel], dict]:
        """
        Searches for `Resource`s that meet the search criteria given.

        Accepts:
            * params (SearchParams): The parameters containing the search
                criteria.
        Returns:
            * resources (Union[QuerySet[ResourceModel], dict]): A collection
                of `Resources` that meet the search criteria in the form
                of either a QuerySet[ResourceModel] or a dictionary which contains
                the `Resource`s in structured form.
        """

        try:

            LOGGER.info(
                f"Searching for Resources with name: {params['name']}, description: "
                f"{params['description']}, functions: {params['functions']}, subfunctions: "
                f"{params['subfunctions']}, employee levels: {params['employee_levels']}, "
                f"tags: {params['tags']}, download: {params['download']}, structure: "
                f"{params['structure']}, serialize: {params['serialize']}, limit: "
                f"{params['limit']}, and page: {params['page']}."
            )

            # Fetch `Resource`s that:
            #  1. Are active.
            #       - The url points to an active site.
            #       - The `Resource` is the most recent revision.
            #  2. Have a linked `Request` whose status is `APPROVED`.
            #       - That `Request` has transitioned through each
            #         stage in the request workflow, receiving all
            #         appropriate dispositions.
            resources: QuerySet[
                ResourceModel, ResourceModel
            ] = ResourceModel.objects.prefetch_related(
                "employee_levels", "subfunctions", "subfunctions__function", "tags"
            ).filter(
                active=True,
                requests__status=Request.RequestStatus.APPROVED,
            )

            # This query is for collecting the ids of the `Resource`s with
            # the highest revision_number for a each uid.
            resource_ids: QuerySet[ResourceModel, ResourceModel] = (
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

            # If either search term exists, perform a contains style search on the
            # respective field.
            if name_search_term or description_search_term:
                search_by_name: QuerySet[ResourceModel] = ResourceModel.objects.none()
                search_by_description: QuerySet[
                    ResourceModel
                ] = ResourceModel.objects.none()

                # If `name_search_term` is non-empty, filter the `Resource`s by name.
                if name_search_term:
                    search_by_name: QuerySet[ResourceModel] = resources.filter(
                        name__icontains=name_search_term
                    )

                # If `description_search_term` is non-empty, filter the `Resource`s by
                # description.
                if description_search_term:
                    search_by_description: QuerySet[ResourceModel] = resources.filter(
                        description__icontains=description_search_term
                    )

                # Union the QuerySets and order by their visit count(descending).
                resources = (
                    (search_by_name | search_by_description)
                    .annotate(visits__count=Count("visits"))
                    .order_by("-visits__count")
                )
            else:
                # Order the `Resource's by their visit count(descending).
                resources = resources.annotate(Count("visits")).order_by(
                    "-visits__count"
                )

            # If `limit` is given, then limit the results.
            resources = resources[: params["limit"]] if params["limit"] else resources

            # Get the page number from `params`.
            page_num: Union[int, None] = params["page"]
            if page_num:
                # Create a Paginator to paginate the collection
                # of `Resource`s.
                paginator: Paginator = Paginator(resources, DEFAULT_PAGE_LENGTH)

                # If `page` number supplied in the params is greater
                # than the number of available pages, then return an
                # empty `Resource` QueryList or dictionary depending on
                # search structure provided.
                if page_num > paginator.num_pages:
                    return (
                        ResourceModel.objects.none()
                        if params["structure"] == utils.DEFAULT_STRUCTURE
                        else {}
                    )

                # Get the corresponding Page
                page: Page = paginator.page(page_num)

                # Assigning the page's `Resource` QueryList to
                # `resources`.
                resources = cast(
                    QuerySet[ResourceModel, ResourceModel], page.object_list
                )

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
            error_msg = f"Missing parameter: `{exc}` from search parameters."
            LOGGER.error(error_msg)
            raise exceptions.DirectoryError(error_msg, status=400) from exc
        except TypeError as exc:
            LOGGER.error(exc)
            error_msg = "Incorrect value given for a search parameter."
            raise exceptions.DirectoryError(error_msg, status=400) from exc
