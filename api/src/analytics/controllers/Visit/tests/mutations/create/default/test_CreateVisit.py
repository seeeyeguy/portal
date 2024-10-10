"""
Collection of pytests for Visit's create controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "analytics",
    "visit",
    "controllers.TestCreateVisit",
    "analytics.visit.create",
    "visit.create.default",
)
class TestCreateVisit(TestCase):
    """Test suite for Visit's create controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.visit.create_visit")
    def test_create_visit(self) -> None:
        """Success Case: Create a `Visit` record."""

    @tag("controllers.visit.create_visit_user_dne")
    def test_create_visit_user_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a user's email where
        that `User` does not exist."""

    @tag("controllers.visit.create_visit_resource_dne")
    def test_create_visit_resource_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a given resource id
        where that `Resource` does not exist."""
