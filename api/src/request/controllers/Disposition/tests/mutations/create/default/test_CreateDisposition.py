"""
Collection of pytests for Disposition's create controller.
"""

import pytest
from typing import cast, List

from django.test import tag

from request import controllers, exceptions, models
from request.controllers.Disposition.tests.mutations.create.default import arguments
from request.models.Disposition.serializers import DispositionSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request",
    "disposition",
    "controllers.TestCreateDisposition",
    "request.disposition.create",
    "disposition.create.default",
)
class TestCreateDisposition(MultiDBTestCase):
    """Test suite for Disposition's create controller."""

    # pylint: disable=line-too-long
    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/users.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/accesses.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/resources.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/resources_error_cases.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/requests.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/requests_error_cases.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/transitions.json",
        "request/controllers/Disposition/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    @tag("controllers.disposition.create_disposition_approved_disposition")
    def test_create_disposition_approved_disposition(self) -> None:
        """Success Case: Create a `Disposition` record approving a
        `Submitted` `Request` as a `Superuser`."""

        # Create `Disposition` record.
        disposition = controllers.Disposition.create_disposition(
            approver=arguments.CREATE_DISPOSITION_USER,
            resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
            disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
        )

        # Fetch approved `Request` record.
        request_record: models.Request = models.Request.objects.only("id").get(
            resource_id=arguments.CREATE_DISPOSITION_RESOURCE_ID,
            status=models.Request.RequestStatus.APPROVED,
        )

        # Fetch latest `Transition` record.
        transition_record: models.Transition | None = (
            models.Transition.objects.filter(request_id=request_record.id)
            .order_by("-created")
            .first()
        )

        self.assertIsInstance(disposition, models.Disposition)
        self.assertIsInstance(transition_record, models.Transition)

        # Serialize `Disposition`.
        serialized_disposition = DispositionSerializer(disposition).data

        # Remove dynamic primary key and datetime fields before comparison.
        del serialized_disposition["id"]
        del serialized_disposition["created"]
        del serialized_disposition["approver"]["access_granted_date"]
        del serialized_disposition["approver"]["access_revoked_date"]
        del serialized_disposition["approver"]["role"]["created"]

        self.assertEqual(
            serialized_disposition,
            arguments.CREATE_DISPOSITION_APPROVED_EXPECTED_VALUES,
        )

        self.assertEqual(
            cast(models.Transition, transition_record).stage.level,
            models.Stage.StageLevels.APPROVED_BY_SUPERUSER,
        )

    @tag("controllers.disposition.create_disposition_rejected_disposition")
    def test_create_disposition_rejected_disposition(self) -> None:
        """Success Case: Create a `Disposition` record rejecting a
        `Request` as a Superuser."""

        # Create `Disposition` record.
        disposition = controllers.Disposition.create_disposition(
            approver=arguments.CREATE_DISPOSITION_USER,
            resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
            disposition=arguments.CREATE_DISPOSITION_REJECTED_DISPOSITION,
            justification=arguments.CREATE_DISPOSITION_REJECTED_JUSTIFICATION,
        )

        # Fetch rejected `Request` record.
        request_record: models.Request = models.Request.objects.only("id").get(
            resource_id=arguments.CREATE_DISPOSITION_RESOURCE_ID,
            status=models.Request.RequestStatus.REJECTED,
        )

        # Fetch latest `Transition` record.
        transition_record: models.Transition | None = (
            models.Transition.objects.filter(request_id=request_record.id)
            .order_by("-created")
            .first()
        )

        self.assertIsInstance(disposition, models.Disposition)
        self.assertIsInstance(transition_record, models.Transition)

        # Serialize `Disposition`.
        serialized_disposition = DispositionSerializer(disposition).data

        # Remove dynamic primary key and datetime fields before comparison.
        del serialized_disposition["id"]
        del serialized_disposition["created"]
        del serialized_disposition["approver"]["access_granted_date"]
        del serialized_disposition["approver"]["access_revoked_date"]
        del serialized_disposition["approver"]["role"]["created"]

        self.assertEqual(
            serialized_disposition,
            arguments.CREATE_DISPOSITION_REJECTED_EXPECTED_VALUES,
        )

        self.assertEqual(
            cast(models.Transition, transition_record).stage.level,
            models.Stage.StageLevels.REJECTED_BY_SUPERUSER,
        )

    @tag("controllers.disposition.create_disposition_revise_disposition")
    def test_create_disposition_revise_disposition(self) -> None:
        """Success Case: Create a `Disposition` record to revise a
        `Request` as a Superuser."""

        # Create `Disposition` record.
        disposition = controllers.Disposition.create_disposition(
            approver=arguments.CREATE_DISPOSITION_USER,
            resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
            disposition=arguments.CREATE_DISPOSITION_REVISE_DISPOSITION,
            justification=arguments.CREATE_DISPOSITION_REVISE_JUSTIFICATION,
        )

        # Fetch pending `Request` record.
        request_record: models.Request = models.Request.objects.only("id").get(
            resource_id=arguments.CREATE_DISPOSITION_RESOURCE_ID,
            status=models.Request.RequestStatus.PENDING,
        )

        # Fetch latest `Transition` record.
        transition_record: models.Transition | None = (
            models.Transition.objects.filter(request_id=request_record.id)
            .order_by("-created")
            .first()
        )

        self.assertIsInstance(disposition, models.Disposition)
        self.assertIsInstance(transition_record, models.Transition)

        # Serialize `Disposition`.
        serialized_disposition = DispositionSerializer(disposition).data

        # Remove dynamic primary key and datetime fields before comparison.
        del serialized_disposition["id"]
        del serialized_disposition["created"]
        del serialized_disposition["approver"]["access_granted_date"]
        del serialized_disposition["approver"]["access_revoked_date"]
        del serialized_disposition["approver"]["role"]["created"]

        self.assertEqual(
            serialized_disposition,
            arguments.CREATE_DISPOSITION_REVISE_EXPECTED_VALUES,
        )

        self.assertEqual(
            cast(models.Transition, transition_record).stage.level,
            models.Stage.StageLevels.DRAFT,
        )

    @tag("controllers.disposition.create_disposition_user_dne")
    def test_create_disposition_user_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a `User`
        that does not exist."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER_DNE,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_resource_dne")
    def test_create_disposition_resource_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` does not exist."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_DNE,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_request_dne")
    def test_create_disposition_request_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` has no pending `Request`."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_REQUEST_DNE,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_transition_dne")
    def test_create_disposition_transition_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where a needed `Transition` record does not exist."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_TRANSITION_DNE,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_active_resource")
    def test_create_disposition_active_resource(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` is already active."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_ACTIVE_RESOURCE_ID,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_historical_resource")
    def test_create_disposition_historical_resource(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` is an inactive previous revision."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_HISTORICAL_RESOURCE_ID,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_revoked_user_access")
    def test_create_disposition_revoked_user_access(self) -> None:
        """Fail Case: Create a `Disposition` record with a `User` whose `Access` is revoked."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_REVOKED_USER_ACCESS,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_invalid_access_for_stage")
    def test_create_disposition_invalid_access_for_stage(self) -> None:
        """Fail Case: Create a `Disposition` record with a `User` that doesn't have
        `Access` to vote on the current `Stage`."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER_INVALID_ACCESS_FOR_STAGE,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_invalid_stage")
    def test_create_disposition_invalid_stage(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where the latest `Transition` is not at a valid voting `Stage`."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_INVALID_STAGE,
                disposition=arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            )

    @tag("controllers.disposition.create_disposition_invalid_disposition")
    def test_create_disposition_invalid_disposition(self) -> None:
        """Fail Case: Create a `Disposition` record with an invalid disposition value."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Disposition.create_disposition(
                approver=arguments.CREATE_DISPOSITION_USER,
                resource=arguments.CREATE_DISPOSITION_RESOURCE_ID,
                disposition=arguments.CREATE_DISPOSITION_INVALID_DISPOSITION,
            )
