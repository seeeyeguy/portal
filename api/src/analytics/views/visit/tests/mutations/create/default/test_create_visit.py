"""Collection of pytests for the Visit's create view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from analytics.controllers.Visit.tests.mutations.create.default import arguments
from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "analytics",
    "visit",
    "views",
    "analytics.visit.create",
    "visit.create.default",
    "views.TestCreateVisit",
)
class TestCreateVisit(TestCase):
    """
    Tests for POST /v1/analytics/visits endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.CREATE_VISIT_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/resources.json",
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/requests.json",
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/transitions.json",
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    url: str = reverse("analytics.visit")

    @tag("views.visit.create_visit")
    def test_create_visit(self) -> None:
        """Success Case: Create a `Visit` record."""

        body: dict = {
            "resource": arguments.CREATE_VISIT_RESOURCE_ID,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        visit = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(visit, dict)

        # Remove dynamic primary key and
        # datetime fields before comparison.
        del visit["id"]
        del visit["created"]

        self.assertEqual(visit, arguments.VALID_CREATED_VISIT)

    @tag("views.visit.create_visit_resource_dne")
    def test_create_visit_resource_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a given resource id
        where that `Resource` does not exist."""

        body: dict = {
            "resource": arguments.CREATE_VISIT_RESOURCE_ID_DNE,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
