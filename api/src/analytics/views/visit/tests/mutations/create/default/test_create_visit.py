"""Collection of pytests for the Visit's create view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

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

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("analytics.visit")

    @tag("views.visit.create_visit")
    def test_create_visit(self) -> None:
        """Success Case: Create a `Visit` record."""

    @tag("views.visit.create_visit_user_dne")
    def test_create_visit_user_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a user's email where
        that `User` does not exist."""

    @tag("views.visit.create_visit_resource_dne")
    def test_create_visit_resource_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a given resource id
        where that `Resource` does not exist."""
