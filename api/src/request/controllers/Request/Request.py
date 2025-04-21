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
from typing import cast, Optional, Tuple, Union

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
from request import exceptions, models
from users import models as UsersModels

LOGGER = logging.getLogger(__name__)


class CreateRequestParams(CreateResourceParams):
    """
    Type annotation for create Request controller
    function params.
    """

    originator: AuthModels.User
    stage: int


class UpdateRequestParams(BaseResourceParams):
    """
    Type annotation for update Request controller
    function params.
    """

    request_id: int
    stage: int


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
            log_msg = (
                f"Creating Request for Resource(name={params['name']}, url={params['url']})"
                f" at Stage(level={params['stage']})"
                f" for Originator(email={params['originator'].email})"
            )
            LOGGER.info(log_msg)

            resource_params = cast(dict, params.copy())
            originator: AuthModels.User = resource_params.pop("originator")
            stage: int = resource_params.pop("stage")
            resource: DirectoryModels.Resource = ResourceController.create_resource(
                cast(CreateResourceParams, resource_params)
            )

            return models.Request()
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
            stage: int = resource_params.pop("stage")

            resource_id: int = 1
            _: Tuple[DirectoryModels.Resource, int] = (
                ResourceController.update_resource(
                    cast(
                        UpdateResourceParams,
                        {"resource_id": resource_id, **resource_params},
                    )
                )
            )

            return models.Request(), 1
        except KeyError as exc:
            err_msg: str = "Invalid parameters given."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 400) from exc
        except DirectoryExceptions.DirectoryError as exc:
            err_msg: str = (
                f"Resource(name={params['name']}, url={params['url']})",
                " for Request was not updated. There is an issue with the Resource's",
                f" attributes. {exc.message}",
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, status=exc.status) from exc

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
