"""
BI Portal `Request` utils module. Common functionality for the
BI Portal `Request` app to help with transitions.
"""

import logging
from typing import cast, Tuple, Union

from django.db.models import Manager

from request import exceptions, models
from users.models.Role.Role import Role

LOGGER = logging.getLogger(__name__)


def transition_request(request_id: int) -> Tuple[models.Request, models.Transition]:
    """Transition a `Request` to the next appropriate stage, given its id."""

    try:
        # Query the `Request` record.
        request_record = models.Request.objects.get(id=request_id)

        # Ensure that the `Request` is pending.
        if request_record.status != models.Request.RequestStatus.PENDING:
            err_msg = f"Request(id={request_id}) is not PENDING."
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 400)

        # Fetch the latest `Transition` record.
        related_transitions = cast(Manager, request_record.transitions)
        latest_transition = cast(
            models.Transition, related_transitions.order_by("-created").first()
        )

        # Check if `Request` is new.
        if not latest_transition:
            # Fetch `Stage` record for `DRAFT` as it is
            # the first appropriate stage.
            draft = models.Stage.objects.get(level=models.Stage.StageLevels.DRAFT)
            # Transition `Request` from `NULL` to `DRAFT`.
            new_transition = models.Transition.objects.create(
                request=request_record,
                stage=draft,
                previous_transition=None,
            )
            return request_record, new_transition

        # Fetch the related `Stage` and `Disposition` for the given `Request`.
        transition_stage = cast(int, latest_transition.stage.level)
        related_dispositions = cast(Manager, latest_transition.dispositions)
        transition_disposition: Union[
            models.Disposition, None
        ] = related_dispositions.first()

        # Ensure `Request` is not in a terminal state.
        if transition_stage in {
            models.Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT,
            models.Stage.StageLevels.APPROVED_BY_SUPERUSER,
            models.Stage.StageLevels.REJECTED_BY_SUPERUSER,
        }:
            err_msg = (
                f"Request(id={request_id}) is in a terminal state"
                f" at Stage(level={transition_stage})."
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 400)

        # Ensure `Request` `Transition` has a `Disposition` if needed.
        if not transition_disposition and transition_stage in {
            models.Stage.StageLevels.SUBMITTED,
            models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
        }:
            err_msg = (
                f"Request(id={request_id}) does not have the needed"
                f" disposition to transition from Stage(level={transition_stage})."
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 409)

        if transition_stage == models.Stage.StageLevels.REVISE:
            # Fetch `Stage` record for `DRAFT` as it is
            # the next appropriate stage.
            draft = models.Stage.objects.get(level=models.Stage.StageLevels.DRAFT)
            # Transition `Request` from `REVISE` to `DRAFT`.
            new_transition = models.Transition.objects.create(
                request=request_record,
                stage=draft,
                previous_transition=latest_transition,
            )
            return request_record, new_transition

        if transition_stage == models.Stage.StageLevels.DRAFT:
            # Fetch `Stage` record for `SUBMITTED` as it is
            # the next appropriate stage.
            submitted = models.Stage.objects.get(
                level=models.Stage.StageLevels.SUBMITTED
            )
            # Transition `Request` from `DRAFT` to `SUBMITTED`.
            new_transition = models.Transition.objects.create(
                request=request_record,
                stage=submitted,
                previous_transition=latest_transition,
            )
            return request_record, new_transition

        transition_disposition = cast(models.Disposition, transition_disposition)
        approver = transition_disposition.approver

        # Ensure that the `Disposition` for the latest `Transition` is valid.
        if (
            transition_stage
            == models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT
            and approver.role.level != Role.RoleLevels.SUPERUSER
        ):
            err_msg = (
                f"Latest Disposition(approver={approver.user.email})"
                f" for Request(id={request_id}) is invalid."
            )
            LOGGER.error(err_msg)
            raise exceptions.RequestError(err_msg, 409)

        if transition_stage == models.Stage.StageLevels.SUBMITTED:
            stage_after_submitted = None
            if (
                transition_disposition.disposition
                == models.Disposition.DispositionValues.REVISE
            ):
                stage_after_submitted = models.Stage.objects.get(
                    level=models.Stage.StageLevels.REVISE
                )

            # Approver is a `Business Process Expert`.
            if approver.role.level == Role.RoleLevels.BUSINESS_PROCESS_EXPERT:
                if (
                    transition_disposition.disposition
                    == models.Disposition.DispositionValues.APPROVED
                ):
                    stage_after_submitted = models.Stage.objects.get(
                        level=models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT
                    )
                if (
                    transition_disposition.disposition
                    == models.Disposition.DispositionValues.REJECTED
                ):
                    stage_after_submitted = models.Stage.objects.get(
                        level=models.Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT
                    )

            # Approver is a `Superuser`.
            if approver.role.level == Role.RoleLevels.SUPERUSER:
                if (
                    transition_disposition.disposition
                    == models.Disposition.DispositionValues.APPROVED
                ):
                    stage_after_submitted = models.Stage.objects.get(
                        level=models.Stage.StageLevels.APPROVED_BY_SUPERUSER
                    )
                if (
                    transition_disposition.disposition
                    == models.Disposition.DispositionValues.REJECTED
                ):
                    stage_after_submitted = models.Stage.objects.get(
                        level=models.Stage.StageLevels.REJECTED_BY_SUPERUSER
                    )

            if not stage_after_submitted:
                err_msg = f"Unable to determine next stage for Request(id={request_id})"
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 409)

            # Transition `Request` from `SUBMITTED` to next appropriate stage.
            new_transition = models.Transition.objects.create(
                request=request_record,
                stage=stage_after_submitted,
                previous_transition=latest_transition,
            )
            return request_record, new_transition

        if (
            transition_stage
            == models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT
        ):
            stage_after_approved_by_business_process_owner = None

            if (
                transition_disposition.disposition
                == models.Disposition.DispositionValues.REVISE
            ):
                # Fetch `Stage` record for `REVISE` as it may be
                # the next appropriate stage.
                stage_after_approved_by_business_process_owner = (
                    models.Stage.objects.get(level=models.Stage.StageLevels.REVISE)
                )

            if (
                transition_disposition.disposition
                == models.Disposition.DispositionValues.APPROVED
            ):
                # Fetch `Stage` record for `APPROVED BY SUPERUSER` as it may be
                # the next appropriate stage.
                stage_after_approved_by_business_process_owner = (
                    models.Stage.objects.get(
                        level=models.Stage.StageLevels.APPROVED_BY_SUPERUSER
                    )
                )

            if (
                transition_disposition.disposition
                == models.Disposition.DispositionValues.REJECTED
            ):
                # Fetch `Stage` record for `REJECTED BY SUPERUSER` as it may be
                # the next appropriate stage.
                stage_after_approved_by_business_process_owner = (
                    models.Stage.objects.get(
                        level=models.Stage.StageLevels.REJECTED_BY_SUPERUSER
                    )
                )

            if not stage_after_approved_by_business_process_owner:
                err_msg = f"Unable to determine next stage for Request(id={request_id})"
                LOGGER.error(err_msg)
                raise exceptions.RequestError(err_msg, 409)

            # Transition `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
            # to the next appropriate stage.
            new_transition = models.Transition.objects.create(
                request=request_record,
                stage=stage_after_approved_by_business_process_owner,
                previous_transition=latest_transition,
            )
            return request_record, new_transition

        err_msg = f"Unable to determine next stage for Request(id={request_id})"
        LOGGER.error(err_msg)
        raise exceptions.RequestError(err_msg, 409)
    except models.Request.DoesNotExist as exc:
        err_msg = f"Request(id={request_id}) for Resource does not exist."
        LOGGER.error(err_msg)
        raise exceptions.RequestError(err_msg, 404) from exc
    except models.Stage.DoesNotExist as exc:
        err_msg = f"Next Stage does not exist. {exc}"
        LOGGER.error(err_msg)
        raise exceptions.RequestError(err_msg, 404) from exc
