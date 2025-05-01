"""
Collection of pytests for the Disposition's
create view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework import status

from request.controllers.Disposition.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "request",
    "disposition",
    "views",
    "request.disposition.create",
    "disposition.create.default",
    "views.TestCreateDisposition",
)
class TestCreateDisposition(MultiDBTestCase):
    """
    Tests for POST /v1/request/disposition endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email=arguments.CREATE_DISPOSITION_USER)
        self.client.force_login(user=user)

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

    url: str = reverse("request.disposition")

    @tag("views.disposition.create_disposition_approved_disposition")
    def test_create_disposition_approved_disposition(self) -> None:
        """Success Case: Create a `Disposition` record approving a `Submitted` `Request`."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")

        disposition = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(disposition, dict)

        # Remove dynamic primary key and datetime fields before comparison.
        del disposition["id"]
        del disposition["created"]
        del disposition["approver"]["access_granted_date"]
        del disposition["approver"]["access_revoked_date"]
        del disposition["approver"]["role"]["created"]

        self.assertEqual(
            disposition, arguments.CREATE_DISPOSITION_APPROVED_EXPECTED_VALUES
        )

    @tag("views.disposition.create_disposition_rejected_disposition")
    def test_create_disposition_rejected_disposition(self) -> None:
        """Success Case: Create a `Disposition` record rejecting a `Submitted` `Request`."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_REJECTED_DISPOSITION,
            "justification": arguments.CREATE_DISPOSITION_REJECTED_JUSTIFICATION,
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")

        disposition = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(disposition, dict)

        # Remove dynamic primary key and datetime fields before comparison.
        del disposition["id"]
        del disposition["created"]
        del disposition["approver"]["access_granted_date"]
        del disposition["approver"]["access_revoked_date"]
        del disposition["approver"]["role"]["created"]

        self.assertEqual(
            disposition, arguments.CREATE_DISPOSITION_REJECTED_EXPECTED_VALUES
        )

    @tag("views.disposition.create_disposition_revise_disposition")
    def test_create_disposition_revise_disposition(self) -> None:
        """Success Case: Create a `Disposition` record to revise a `Submitted` `Request`."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_REVISE_DISPOSITION,
            "justification": arguments.CREATE_DISPOSITION_REVISE_JUSTIFICATION,
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")

        disposition = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(disposition, dict)

        # Remove dynamic primary key and datetime fields before comparison.
        del disposition["id"]
        del disposition["created"]
        del disposition["approver"]["access_granted_date"]
        del disposition["approver"]["access_revoked_date"]
        del disposition["approver"]["role"]["created"]

        self.assertEqual(
            disposition, arguments.CREATE_DISPOSITION_REVISE_EXPECTED_VALUES
        )

    @tag("views.disposition.create_disposition_resource_dne")
    def test_create_disposition_resource_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` does not exist."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_DNE,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.disposition.create_disposition_request_dne")
    def test_create_disposition_request_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` has no pending `Request`."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_REQUEST_DNE,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.disposition.create_disposition_transition_dne")
    def test_create_disposition_transition_dne(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where a needed `Transition` record does not exist."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_TRANSITION_DNE,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 409.
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @tag("views.disposition.create_disposition_active_resource")
    def test_create_disposition_active_resource(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` is already active."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_ACTIVE_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.disposition.create_disposition_historical_resource")
    def test_create_disposition_historical_resource(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where that `Resource` is an inactive previous revision."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_HISTORICAL_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.disposition.create_disposition_revoked_user_access")
    def test_create_disposition_revoked_user_access(self) -> None:
        """Fail Case: Create a `Disposition` record with a `User` whose `Access` is revoked."""

        user = User.objects.get(email=arguments.CREATE_DISPOSITION_REVOKED_USER_ACCESS)
        self.client.force_login(user=user)

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 403.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.disposition.create_disposition_invalid_access_for_stage")
    def test_create_disposition_invalid_access_for_stage(self) -> None:
        """Fail Case: Create a `Disposition` record with a `User` that doesn't have
        `Access` to vote on the current `Stage`."""

        user = User.objects.get(
            email=arguments.CREATE_DISPOSITION_USER_INVALID_ACCESS_FOR_STAGE
        )
        self.client.force_login(user=user)

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 403.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.disposition.create_disposition_invalid_stage")
    def test_create_disposition_transition_invalid_stage(self) -> None:
        """Fail Case: Create a `Disposition` record with a given resource id
        where the latest `Transition` is not at a valid voting `Stage`."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_INVALID_STAGE,
            "disposition": arguments.CREATE_DISPOSITION_APPROVED_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.disposition.create_disposition_invalid_disposition")
    def test_create_disposition_transition_invalid_disposition(self) -> None:
        """Fail Case: Create a `Disposition` record with an invalid disposition value."""

        body: dict = {
            "resource_id": arguments.CREATE_DISPOSITION_RESOURCE_ID,
            "disposition": arguments.CREATE_DISPOSITION_INVALID_DISPOSITION,
            "justification": "",
        }

        # Make request to create `Disposition`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
