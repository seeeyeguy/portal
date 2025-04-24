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
from request import exceptions, models
from request.utils import transitions
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
        approver: str, resource: int, disposition: str, justification: str = ""
    ) -> models.Disposition:
        """
        Create a `Disposition` record in the database using the given
        user, resource id, disposition, and justification.

        Accepts:
            * approver (str): The user that approved the given resource.
            * resource (int): The id of the resource being created/modified.
            * disposition (str): The vote being recorded. This
                can be `APPROVED`, `REJECTED`, `REVISE`, etc.
            * justification (str): The reason as to why a disposition
                other than `APPROVED` is recorded.

        Returns:
            * disposition (models.Disposition): The newly created `Disposition`
                record.
        """

        log_msg: str = f"Creating Disposition: {disposition} for User: {approver} and Resource: {resource}."

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
                    f"Disposition: {disposition} is not valid. "
                    f"Disposition must be {models.Disposition.DispositionValues.APPROVED}, "
                    f"{models.Disposition.DispositionValues.REJECTED} "
                    f"or {models.Disposition.DispositionValues.REVISE}."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Fetch `User` record.
            user_record: User = User.objects.only("username").get(
                email__iexact=approver
            )

            # Construct list of `Role`s allowed to create a `Disposition`.
            valid_approvers: List[int] = [
                UsersModels.Role.RoleLevels.SUPERUSER,
                UsersModels.Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
            ]

            # Fetch `Access` record.
            access_record: Union[UsersModels.Access, None] = (
                UsersModels.Access.objects.filter(
                    user_id=user_record.username,
                    access_revoked_date__isnull=True,
                    role__level__in=valid_approvers,
                )
                .order_by("role__level")
                .first()
            )

            if not access_record:
                err_msg = "Permissions denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Fetch inactive `Resource` record.
            resource_record: Resource = Resource.objects.only("id").get(
                id=resource, active=False
            )

            # Fetch pending `Request` record.
            request_record: models.Request = models.Request.objects.select_related(
                "originator__user"
            ).get(
                resource_id=resource_record.id,
                status=models.Request.RequestStatus.PENDING,
            )

            # Fetch latest `Transition` record.
            transition_record: Union[models.Transition, None] = (
                models.Transition.objects.filter(request_id=request_record.id)
                .order_by("-created")
                .first()
            )

            # Ensure a `Transition` record exists.
            if not transition_record:
                err_msg = (
                    f"Transition for Resource"
                    f"(id={resource_record.id}, name={resource_record.name}, url={resource_record.url}) "
                    "does not exist."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 409)

            # Ensure latest `Transition` corresponds to a valid voting `Stage`.
            if transition_record.stage.level not in [
                models.Stage.StageLevels.SUBMITTED,
                models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
            ]:
                err_msg = (
                    f"Disposition cannot be recorded for Resource"
                    f"(id={resource_record.id}, name={resource_record.name}, url={resource_record.url}) "
                    f"in Stage: {transition_record.stage.name}."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            # Ensure `User` has an `Access` to vote on the current `Stage`.
            if not access_record.stage.filter(
                level=transition_record.stage.level
            ).exists():
                err_msg = "Permissions denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Ensure `User` cannot vote on their own `Request`.
            if user_record.email == request_record.originator.user.email:
                err_msg = "Permissions denied."
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 403)

            # Ensure `Disposition` record doesn't already exist for the
            # latest `Transition` for the given `Resource`.
            if models.Disposition.objects.filter(
                transition_id=transition_record.id,
            ).exists():
                err_msg = (
                    f"Disposition: {disposition.upper()} already exists for Resource"
                    f"(id={resource_record.id}, name={resource_record.name}, url={resource_record.url}) "
                    f"at Stage: {transition_record.stage.name}."
                )
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 400)

            with transaction.atomic():
                # Create `Disposition` record for the given `User` and `Resource`.
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
                request_record, new_transition = transitions.transition_request(
                    request_record.id
                )

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
                elif stage_record.level in [
                    models.Stage.StageLevels.REJECTED_BY_SUPERUSER,
                    models.Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT,
                ]:
                    new_request_status = "REJECTED"
                else:
                    # Transition the `Request` from `REVISE` to `DRAFT`.
                    if stage_record.level == models.Stage.StageLevels.REVISE:
                        _ = transitions.transition_request(request_record.id)

                    return disposition_record

                # Update `Request` record.
                request_record.status = new_request_status
                request_record.save()

            return disposition_record

        except User.DoesNotExist as exc:
            err_msg = f"User (email={approver}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 404) from exc
        except Resource.DoesNotExist as exc:
            err_msg = f"A pending Resource (id={resource}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 404) from exc
        except models.Request.DoesNotExist as exc:
            err_msg = f"A pending Request for Resource (id={resource}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 404) from exc
