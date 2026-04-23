"""
`BI Portal` `Disposition` controller module. Controllers utilize the
Django ORM to create and fetch records within the `Disposition` table.
`Disposition` represents a vote by a BI Portal admin on a
request to add/modify a directory resource.
"""

import logging
from typing import List, Union

from django.contrib.auth.models import User
from django.db import transaction

from directory.models import Resource
from portal.mail.helpers.request_queue_email import queue_originator_status_change_email
from request import exceptions, models
from request.utils.transitions import transition_request
from users import models as UsersModels

LOGGER = logging.getLogger(__name__)


class Disposition:
    """
    Container class for functions related to creating
    and fetching `Disposition` records. `Disposition`
    represents a vote by a BI Portal admin on a
    request to add/modify a directory resource.
    """

    @staticmethod
    def create_disposition(
        approver: User, request: int, disposition: str, justification: str = ""
    ) -> models.Disposition:
        """
        Create a `Disposition` record in the database using the given
        user, request id, disposition, and justification.

        Accepts:
            * approver (auth.User): The user approving the given request.
            * request (int): The id of the request to be considered.
            * disposition (str): The vote being recorded. This
                can be `APPROVED`, `REJECTED`, `REVISE`, etc.
            * justification (str): The reason as to why a disposition
                other than `APPROVED` is recorded.

        Returns:
            * disposition (models.Disposition): The newly created `Disposition`
                record.
        """

        approver_username: str = (
            approver.username if approver.is_authenticated else None
        )

        log_msg: str = (
            f"Creating Disposition (disposition={disposition})"
            f" for Request (id={request}) by User (username={approver_username})."
        )

        if justification:
            log_msg = f"{log_msg} Justification: {justification}"

        LOGGER.info(log_msg)

        try:
            # Ensure the vote being recorded is valid.
            if disposition.upper() not in [
                models.Disposition.DispositionValues.APPROVED,
                models.Disposition.DispositionValues.REJECTED,
                models.Disposition.DispositionValues.REVISE,
            ]:
                err_msg = (
                    f"Disposition ({disposition}) is not valid. "
                    f"Disposition must be {models.Disposition.DispositionValues.APPROVED}, "
                    f"{models.Disposition.DispositionValues.REJECTED} "
                    f"or {models.Disposition.DispositionValues.REVISE}."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Construct list of `Role`s allowed to create a `Disposition`.
            valid_approvers: List[int] = [
                UsersModels.Role.RoleLevels.SUPERUSER,
                UsersModels.Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
            ]

            if not (approver and approver.is_authenticated):
                err_msg = "Authentication required."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 401)

            # Fetch `Access` record.
            access_record: Union[UsersModels.Access, None] = (
                UsersModels.Access.objects.filter(
                    user=approver,
                    access_revoked_date__isnull=True,
                    role__level__in=valid_approvers,
                )
                .order_by("role__level")
                .first()
            )

            if not access_record:
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Fetch pending `Request` record.
            request_record: models.Request = models.Request.objects.select_related(
                "originator__user"
            ).get(id=request)

            if request_record.status in {
                models.Request.RequestStatus.APPROVED,
                models.Request.RequestStatus.REJECTED,
            }:
                err_msg = f"Request (id={request}) is not {models.Request.RequestStatus.PENDING}."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Fetch `Resource` record related to request.
            resource_record: Resource = request_record.resource

            if resource_record.active:
                err_msg = (
                    f"Resource (id={resource_record.id})"
                    f" for Request (id={request}) is already active."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Fetch latest `Transition` record.
            transition_record: Union[models.Transition, None] = (
                models.Transition.objects.filter(request_id=request_record.id)
                .order_by("-created")
                .first()
            )

            # Ensure a `Transition` record exists.
            if not transition_record:
                err_msg = f"Transition for Request (id={request}) does not exist."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 409)

            # Ensure latest `Transition` corresponds to a valid voting `Stage`.
            if transition_record.stage.level not in [
                models.Stage.StageLevels.SUBMITTED,
                models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
            ]:
                err_msg = (
                    "Disposition is not permitted at"
                    f" Stage (name={transition_record.stage.name})."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Ensure `User` has an `Access` to vote on `Request`s for `Resource`s
            # within the related `SubFunction`s.
            is_superuser = (
                access_record.role.level == UsersModels.Role.RoleLevels.SUPERUSER
            )
            has_subfunction_permissions = access_record.subfunctions.filter(
                id__in=resource_record.subfunctions.values_list("id", flat=True)
            ).exists()
            if not (is_superuser or has_subfunction_permissions):
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Ensure `User` has an `Access` to vote at the current `Stage`.
            if not access_record.stage.filter(
                level=transition_record.stage.level
            ).exists():
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Ensure `User` cannot approve their own `Request`.
            if (
                approver.email == request_record.originator.user.email
                and disposition.upper() == models.Disposition.DispositionValues.APPROVED
            ):
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Ensure `Disposition` record doesn't already exist for the
            # latest `Transition`.
            if models.Disposition.objects.filter(
                transition_id=transition_record.id,
            ).exists():
                err_msg = (
                    f"Disposition already exists for Request (id={request})"
                    f"at Stage (name={transition_record.stage.name})."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            with transaction.atomic():
                # Create `Disposition` record for the given `User` and `Request`.
                disposition_record: models.Disposition = (
                    models.Disposition.objects.create(
                        approver_id=access_record.id,
                        disposition=disposition.upper(),
                        justification=(
                            justification
                            if disposition.upper()
                            != models.Disposition.DispositionValues.APPROVED
                            else ""
                        ),
                        transition_id=transition_record.id,
                    )
                )

                # Transition the `Request`.
                request_record, new_transition = transition_request(request_record.id)

                # Fetch `Stage` corresponding to the new stage.
                stage_record = new_transition.stage

                # Determine new `Request` status based on the new `Stage`.
                new_request_status = "PENDING"
                if stage_record.level == models.Stage.StageLevels.APPROVED_BY_SUPERUSER:
                    new_request_status = "APPROVED"
                    new_resource_revision = 1

                    # Deprecate previous `Resource` revision if it exists.
                    previous_resource_revision: Union[
                        Resource, None
                    ] = resource_record.previous_revision
                    if previous_resource_revision:
                        previous_resource_revision.active = False
                        new_resource_revision = (
                            previous_resource_revision.revision_number + 1
                        )
                        previous_resource_revision.save()

                    # Update `Resource` record.
                    resource_record.active = True
                    resource_record.revision_number = new_resource_revision
                    resource_record.save()

                    # Send approval email to originator
                    try:
                        queue_originator_status_change_email(request_record, "approved")
                        LOGGER.info(
                            f"Queued approval email for Request (id={request_record.id})"
                        )
                    except Exception as email_exc:
                        LOGGER.error(f"Failed to queue approval email: {email_exc}")

                elif stage_record.level in [
                    models.Stage.StageLevels.REJECTED_BY_SUPERUSER,
                    models.Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT,
                ]:
                    new_request_status = "REJECTED"

                    # Send rejection email to originator
                    try:
                        queue_originator_status_change_email(request_record, "rejected")
                        LOGGER.info(
                            f"Queued rejection email for Request (id={request_record.id})"
                        )
                    except Exception as email_exc:
                        LOGGER.error(f"Failed to queue rejection email: {email_exc}")

                else:
                    # Transition the `Request` from `REVISE` to `DRAFT`.
                    if stage_record.level == models.Stage.StageLevels.REVISE:
                        # Send revision email to originator
                        try:
                            queue_originator_status_change_email(
                                request_record, "revised"
                            )
                            LOGGER.info(
                                f"Queued revision email for Request (id={request_record.id})"
                            )
                        except Exception as email_exc:
                            LOGGER.error(f"Failed to queue revision email: {email_exc}")

                        _ = transition_request(request_record.id)

                    return disposition_record

                # Update `Request` record.
                request_record.status = new_request_status
                request_record.save()

            return disposition_record
        except models.Request.DoesNotExist as exc:
            err_msg = f"A pending Request (id={request}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 404) from exc
