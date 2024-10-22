"""
Collection of pytests for Visit's create controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.test import tag, TestCase

from analytics.controllers.Visit.Visit import Visit
from analytics.controllers.Visit.tests.mutations.create.default import arguments
from analytics.exceptions import AnalyticsError
from analytics.models.Visit.Visit import Visit as VisitModel
from analytics.models.Visit.serializers import VisitSerializer


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

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/resources.json",
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/requests.json",
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/transitions.json",
        "analytics/controllers/Visit/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    @tag("controllers.visit.create_visit")
    def test_create_visit(self) -> None:
        """Success Case: Create a `Visit` record."""

        visit = Visit.create_visit(
            user=arguments.CREATE_VISIT_USER_EMAIL,
            resource=arguments.CREATE_VISIT_RESOURCE_ID,
        )

        self.assertIsInstance(visit, VisitModel)

        # Serialize `Visit`.
        serialized_visit: dict = VisitSerializer(visit).data

        # Remove dynamic primary key and
        # datetime fields before comparison.
        del serialized_visit["id"]
        del serialized_visit["created"]

        self.assertEqual(serialized_visit, arguments.VALID_CREATED_VISIT)

    @tag("controllers.visit.create_visit_user_dne")
    def test_create_visit_user_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a user's email where
        that `User` does not exist."""

        with pytest.raises(AnalyticsError):
            _ = Visit.create_visit(
                user=arguments.CREATE_VISIT_USER_EMAIL_DNE,
                resource=arguments.CREATE_VISIT_RESOURCE_ID,
            )

    @tag("controllers.visit.create_visit_resource_dne")
    def test_create_visit_resource_dne(self) -> None:
        """Fail Case: Create a `Visit` record with a given resource id
        where that `Resource` does not exist."""

        with pytest.raises(AnalyticsError):
            _ = Visit.create_visit(
                user=arguments.CREATE_VISIT_USER_EMAIL,
                resource=arguments.CREATE_VISIT_RESOURCE_ID_DNE,
            )
