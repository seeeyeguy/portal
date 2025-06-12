"""
`BI Portal` `Request` controller module. Controllers create,
fetch, and update records within the `Request` table. `Request`
represent a request by a `User` to create, update, or delete
a `Resource` record within `BI Portal`. A `Resource` record
must be related to a `Request` that has been processed through
the `BI Portal` request workflow with the needed approvals
before any change can be made in `BI Portal`'s published
`Resource` record dataset.
"""

import logging
from typing import cast, Optional, Tuple, TypedDict, Union

# NEED TO REMOVE pylint-disable AFTER IMPLEMENTATION.
# pylint: disable=unused-argument,unused-variable,logging-fstring-interpolation,no-member
from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet

from directory.controllers.Resource.Resource import (
    BaseResourceParams,
    CreateResourceParams,
    Resource as ResourceController,
    UpdateResourceParams,
)


from directory import exceptions as DirectoryExceptions, models as DirectoryModels
from directory.models.Resource.serializers import ResourceSerializer
from request import exceptions, models
from request.utils.transitions import transition_request
from users import models as UsersModels


LOGGER = logging.getLogger(__name__)

DRAFT = "DRAFT"
SUBMITTED = "SUBMITTED"


class CreateRequestParams(CreateResourceParams):
    """
    Type annotation for create Request controller
    function params.
    """

    originator: AuthModels.User
    stage: str


class UpdateRequestParams(BaseResourceParams):
    """
    Type annotation for update Request controller
    function params.
    """

    request_id: int
    stage: str


class DeleteRequestParams(TypedDict):
    """
    Type annotation for delete Request controller
    function params.
    """

    resource_id: int
    originator: AuthModels.User


class Request:
    """
    Container class for functions related to creating, updating, and
    retrieving `Request` records. `Request` represents a request by
    a `User` to create, update, or delete a `Resource` record
    within `BI Portal`.
    """

    @staticmethod
    def create_request(params: CreateRequestParams) -> models.Request:
        """
        Create a `Request` and related `Resource` record with
        the given params.

        Accepts:
            * params (CreateRequestParams): The parameters used to create
                a `Request` and related `Resource` record.

        Returns:
            * request (models.Request): The new `Request` record.
        """

        try:
            resource_params = cast(dict, params.copy())

            stage: str = resource_params.pop("stage")

            log_msg = (
                f"{'Creating' if stage != SUBMITTED else 'Submitting'}"
                f" Request for Resource(name={params['name']}, url={params['url']})"
                f" for Originator(email={params['originator'].email})."
            )
            LOGGER.info(log_msg)

            # Fetch `Access` record for originator.
            originator: AuthModels.User = resource_params.pop("originator")
            accepted_roles = [
                UsersModels.Role.RoleLevels.DATA_STEWARD,
                UsersModels.Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
                UsersModels.Role.RoleLevels.SUPERUSER,
            ]
            originator_access: Union[UsersModels.Access, None] = (
                UsersModels.Access.objects.filter(
                    user=originator,
                    role__level__in=accepted_roles,
                    access_revoked_date__isnull=True,
                )
                .order_by("-role__level")
                .first()
            )

            # Ensure originator has the appropriate permissions.
            if not originator_access:
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            if stage not in [DRAFT, SUBMITTED]:
                err_msg = f"Stage must be {DRAFT} or {SUBMITTED}."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Create the related `Resource` record.
            resource: DirectoryModels.Resource = ResourceController.create_resource(
                cast(CreateResourceParams, resource_params)
            )

            # Create the `Request` record.
            request = models.Request.objects.create(
                resource=resource,
                originator=originator_access,
                status=models.Request.RequestStatus.PENDING,
            )

            # Transition `Request` to `DRAFT`.
            transition_request(request_id=request.id)

            # If the `Request` was submitted on create,
            # transition `Request` to `SUBMITTED`.
            if stage == SUBMITTED:
                transition_request(request_id=request.id)

            return request
        except KeyError as exc:
            err_msg: str = "Invalid parameters given."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 400) from exc
        except DirectoryExceptions.DirectoryError as exc:
            err_msg: str = (
                f"Resource(name={params['name']}, url={params['url']})",
                " for Request was not created. There is an issue with the Resource's",
                f" attributes. {exc.message}",
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=exc.status) from exc

    @staticmethod
    def update_request(params: UpdateRequestParams) -> Tuple[models.Request, int]:
        """
        Update a `Request` and related `Resource` record with
        the given params.

        Accepts:
            * params (UpdateRequestParams): The parameters used to update
                a `Request` and related `Resource` record.

        Returns:
            * request (models.Request): The updated `Request` record.
            * rows_affected (int): The number of rows updated.
        """

        try:
            log_msg = (
                f"Updating Request(id={params['request_id']}) for"
                f" Resource(name={params['name']}, url={params['url']})"
                f" at Stage(level={params['stage']})"
            )
            LOGGER.info(log_msg)

            resource_params = cast(dict, params.copy())
            request_id: int = resource_params.pop("request_id")
            stage: str = resource_params.pop("stage")

            # Fetch the existing `Request` record.
            request = models.Request.objects.get(id=request_id)

            # Fetch `Access` record for requester.
            requester: AuthModels.User = resource_params.pop("user")
            accepted_roles = [
                UsersModels.Role.RoleLevels.DATA_STEWARD,
                UsersModels.Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
                UsersModels.Role.RoleLevels.SUPERUSER,
            ]
            requester_access: Union[UsersModels.Access, None] = (
                UsersModels.Access.objects.filter(
                    user=requester,
                    role__level__in=accepted_roles,
                    access_revoked_date__isnull=True,
                )
                .order_by("-role__level")
                .first()
            )

            # Ensure originator has the appropriate permissions.
            if not requester_access:
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Validate the `stage` parameter.
            if stage not in [DRAFT, SUBMITTED]:
                err_msg = f"Stage must be {DRAFT} or {SUBMITTED}."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Validate the requester and originator are the same.
            if requester_access.user != request.originator.user:
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Fetch the latest `Transition` record.
            latest_transition = cast(
                models.Transition, request.transitions.order_by("-created").first()
            )

            # Ensure `Request` is at the `DRAFT` stage
            if (
                not latest_transition
                or latest_transition.stage.level != models.Stage.StageLevels.DRAFT
            ):
                err_msg = f"Request(id={request_id}) must be in {DRAFT}."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Update the related `Resource` record.
            resource_id: int = request.resource.id
            _, rows_affected = ResourceController.update_resource(
                cast(
                    UpdateResourceParams,
                    {
                        "resource_id": resource_id,
                        "user": requester_access.user,
                        **resource_params,
                    },
                )
            )

            # If the `Request` was submitted on update,
            # transition `Request` to `SUBMITTED`.
            if stage == SUBMITTED:
                _, _ = transition_request(request_id=request.id)

            # Refresh the `Request` record.
            request.refresh_from_db()
            return request, rows_affected
        except KeyError as exc:
            err_msg: str = "Invalid parameters given."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 400) from exc
        except models.Request.DoesNotExist as exc:
            err_msg: str = f"Request(id={params['request_id']}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 404) from exc
        except DirectoryExceptions.DirectoryError as exc:
            err_msg: str = (
                f"Resource(name={params['name']}, url={params['url']})",
                " for Request was not updated. There is an issue with the Resource's",
                f" attributes. {exc.message}",
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=exc.status) from exc

    @staticmethod
    def delete_request(params: DeleteRequestParams) -> models.Request:
        """
        Create a `Request` to delete a `Resource` record with
        the given params.

        Accepts:
            * params (DeleteRequestParams): The parameters used to create
                a `Request` to delete a related `Resource` record.

        Returns:
            * request (models.Request): The new `Request` record.
        """

        try:
            resource_params = cast(dict, params.copy())

            log_msg = (
                f" Creating a Request to delete"
                f" Resource(id={params['resource_id']})"
                f" for Originator(email={params['originator']})."
            )
            LOGGER.info(log_msg)

            # Fetch `Access` record for originator.
            originator: AuthModels.User = resource_params.pop("originator")
            accepted_roles = [
                UsersModels.Role.RoleLevels.DATA_STEWARD,
                UsersModels.Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
                UsersModels.Role.RoleLevels.SUPERUSER,
            ]
            originator_access: Union[UsersModels.Access, None] = (
                UsersModels.Access.objects.filter(
                    user=originator,
                    role__level__in=accepted_roles,
                    access_revoked_date__isnull=True,
                )
                .order_by("-role__level")
                .first()
            )

            # Ensure originator has the appropriate permissions.
            if not originator_access:
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            resource_id: int = resource_params.pop("resource_id")

            resource_record = DirectoryModels.Resource.objects.get(id=resource_id)

            delete_resource_params = ResourceSerializer(resource_record).data

            # Remove unused properties.
            delete_resource_params.pop("id")
            delete_resource_params.pop("active")
            point_of_contacts = [delete_resource_params.pop("primary_point_of_contact")]

            # Flatten employee levels.
            employee_levels = [
                level["id"]
                for level in delete_resource_params.get("employee_levels", [])
            ]

            # Flatten subfunctions.
            subfunctions = [
                subfunction["id"]
                for subfunction in delete_resource_params.get("subfunctions", [])
            ]

            # Flatten tags.
            tags = [tag["id"] for tag in delete_resource_params.get("tags", [])]

            # Update properties.
            delete_resource_params.update(
                {
                    # Updated.
                    "previous_revision": resource_id,
                    "deleted": True,
                    "user": originator,
                    # Flattened.
                    "point_of_contacts": point_of_contacts,
                    "employee_levels": employee_levels,
                    "subfunctions": subfunctions,
                    "tags": tags,
                }
            )

            # Create the related `Resource` record.
            resource: DirectoryModels.Resource = ResourceController.create_resource(
                cast(CreateResourceParams, delete_resource_params)
            )

            # Create the `Request` record.
            request = models.Request.objects.create(
                resource=resource,
                originator=originator_access,
                status=models.Request.RequestStatus.PENDING,
            )

            # Transition `Request` to `DRAFT`.
            transition_request(request_id=request.id)

            # Transition `Request` to `SUBMITTED`.
            transition_request(request_id=request.id)

            return request
        except KeyError as exc:
            err_msg: str = f"Invalid parameters given. {exc}"
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 400) from exc
        except DirectoryExceptions.DirectoryError as exc:
            err_msg: str = (
                f"Resource(id={params['resource_id']})",
                " for Request was not created. There is an issue with the Resource's",
                f" attributes. {exc.message}",
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=exc.status) from exc
        except DirectoryModels.Resource.DoesNotExist as exc:
            err_msg = f"Resource (id={params['resource_id']}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 404) from exc

    @staticmethod
    def fetch_requests(
        request_id: Optional[int] = None,
        originator: Optional[str] = None,
        stage: Optional[int] = None,
        status: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        include_archived: Optional[bool] = False,
    ) -> Union[models.Request, QuerySet[models.Request]]:
        """
        Fetch a `Request` record from the database with the given id
        or if no id is specified return all `Request` records. If
        `originator`, `stage` or `status` is provided, filter records
        appropriately. If page is specified, return that page of records.
        If limit is specified, return up to `limit` number of records.

        Accepts:
            * request_id (int | None): Optional parameter to either return a
                single `Request` record with that specified id or all `Request`
                records from the database if `None`.
            * originator (str | None): Optional parameter to filter
                `Request` records by the `originator`. If specified, we will only
                return `Request` records related to the given `originator`
                (i.e the user that made the request).
            * stage (int | None): Optional parameter to filter `Request` records
                by their current stage. If specified, we will only return `Request`
                records at the given `stage`.
            * status (str): Optional parameter to filter `Request` records by their
                status. A `Request` status may be `PENDING`, `APPROVED` or `REJECTED`.
                If specified, we will only return `Request` records with the given
                `status`.
            * page (int | None): The page of `Request` records to return.
            * limit (int | None): The limit of `Request` records to return.
            * include_archived (bool): Whether to include `Request` records related
                to historical `Resources`.
        """

        try:
            originator_email: str = originator if originator else "None"
            msg_params = [
                (
                    originator,
                    lambda m: f"{m} with originator(email={originator_email})",
                ),
                (stage, lambda m: f"{m} at stage(level={stage})"),
                (status, lambda m: f"{m} with status: {status}"),
                (page, lambda m: f"{m} with page: {page}"),
                (limit, lambda m: f"{m} {'and' if page else 'with'} limit: {limit}"),
            ]
            log_msg = "s"
            for value, message in msg_params:
                if value:
                    log_msg = message(log_msg)

            if request_id:
                log_msg = f" with id: {request_id}"

            LOGGER.info(f"Fetching `Request` record{log_msg}.")

            requests = models.Request.objects.all()

            return requests
        except models.Request.DoesNotExist as exc:
            err_msg: str = f"Request(id={request_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=404) from exc
        except AuthModels.User.DoesNotExist as exc:
            err_msg: str = f"Originator(email={originator}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=404) from exc
        except UsersModels.Access.DoesNotExist as exc:
            err_msg: str = f"Originator(email={originator}) has not created a request."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=400) from exc
