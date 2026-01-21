from typing import List

from django.test import tag
from directory.models import Resource
from analytics.controllers.Visit.Visit import Visit
from manager.utils.tests import MultiDBTestCase
from portal.models.fixtures import COMMON_FIXTURES

# import shared arguments
from analytics.controllers.Visit.tests.query.read.default import arguments


@tag(
    "controllers",
    "analytics",
    "visit",
    "controllers.TestFetchVisit",
    "analytics.visit.fetch",
    "visit.fetch.default",
)
class TestFetchVisit(MultiDBTestCase):
    """Test suite for Visit's fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Visit/tests/query/read/default/fixtures/resources.json",
        "analytics/controllers/Visit/tests/query/read/default/fixtures/visits.json",
    ]

    def setUp(self) -> None:
        """Load fixture data for testing."""
        self.resource = Resource.objects.get(pk=arguments.FETCH_VISIT_BY_RESOURCE_ID)

    @tag("controllers.Visit.fetch_visited_resource")
    def test_fetch_visit(self) -> None:
        """Success Case: Fetch all `Visit` records."""
        visits = Visit.fetch_visited_resource(user="", resource=None)
        self.assertGreaterEqual(len(visits), arguments.FETCH_VISIT_RECORD_COUNT)
        self.assertIn("visit_count", visits[0])

    @tag("controllers.Visit.fetch_visited_resource_with_page")
    def test_fetch_visit_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records."""
        visits = Visit.fetch_visited_resource(
            user="",
            resource=None,
            page=arguments.FETCH_VISIT_WITH_PAGE,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_WITH_PAGE_RECORD_COUNT)

    # --- Limit ---
    @tag("controllers.Visit.fetch_visited_resource_with_limit")
    def test_fetch_visit_with_limit(self) -> None:
        """Success Case: Fetch all `Visit` records up to limit."""
        visits = Visit.fetch_visited_resource(
            user="",
            resource=None,
            page=arguments.FETCH_VISIT_WITH_PAGE,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_WITH_LIMIT_RECORD_COUNT)

    @tag("controllers.Visit.fetch_visited_resource_with_page_and_limit")
    def test_fetch_visit_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records up to limit."""
        visits = Visit.fetch_visited_resource(
            user="",
            resource=None,
            page=arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(
            len(visits), arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT_RECORD_COUNT
        )

    @tag("controllers.Visit.fetch_visited_resource_by_user")
    def test_fetch_visit_by_user(self) -> None:
        """Success Case: Fetch `Visit` records given a username"""
        visits = Visit.fetch_visited_resource(
            user=arguments.FETCH_VISIT_BY_USER, resource=None
        )
        # May Parker has visits on 2 resources
        self.assertEqual(len(visits), 2)
        counts = {v["resource"]["id"]: v["visit_count"] for v in visits}
        self.assertEqual(counts[1], 2)  # Resource 1 has 2 visits
        self.assertEqual(counts[2], 1)  # Resource 2 has 1 visit

    @tag("controllers.Visit.fetch_visited_resource_by_user_with_page")
    def test_fetch_visit_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a username"""
        visits = Visit.fetch_visited_resource(
            user=arguments.FETCH_VISIT_BY_USER,
            resource=None,
            page=arguments.FETCH_VISIT_WITH_PAGE,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_WITH_PAGE_RECORD_COUNT)

    @tag("controllers.Visit.fetch_visited_resource_by_user_with_limit")
    def test_fetch_visit_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a username up to limit."""
        visits = Visit.fetch_visited_resource(
            user=arguments.FETCH_VISIT_BY_USER,
            resource=None,
            page=arguments.FETCH_VISIT_WITH_PAGE,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_WITH_LIMIT_RECORD_COUNT)

    @tag("controllers.Visit.fetch_visited_resource_by_user_with_page_and_limit")
    def test_fetch_visit_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a username up to limit."""
        visits = Visit.fetch_visited_resource(
            user=arguments.FETCH_VISIT_BY_USER,
            resource=None,
            page=arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(
            len(visits), arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT_RECORD_COUNT
        )

    @tag("controllers.Visit.fetch_visited_resource_by_resource")
    def test_fetch_visit_by_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id."""
        visits = Visit.fetch_visited_resource(
            user="", resource=arguments.FETCH_VISIT_BY_RESOURCE_ID
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_BY_RESOURCE_RECORD_COUNT)
        self.assertEqual(visits[0]["resource"]["id"], self.resource.id)

    @tag("controllers.Visit.fetch_visited_resource_by_resource_with_page")
    def test_fetch_visit_by_resource_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a `Resource`'s id."""
        visits = Visit.fetch_visited_resource(
            user="",
            resource=arguments.FETCH_VISIT_BY_RESOURCE_ID,
            page=arguments.FETCH_VISIT_WITH_PAGE,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_WITH_PAGE_RECORD_COUNT)

    @tag("controllers.Visit.fetch_visited_resource_by_resource_with_limit")
    def test_fetch_visit_by_resource_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id up to limit."""
        visits = Visit.fetch_visited_resource(
            user="",
            resource=arguments.FETCH_VISIT_BY_RESOURCE_ID,
            page=arguments.FETCH_VISIT_WITH_PAGE,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(len(visits), arguments.FETCH_VISIT_WITH_LIMIT_RECORD_COUNT)

    @tag("controllers.Visit.fetch_visited_resource_by_resource_with_page_and_limit")
    def test_fetch_visit_by_resource_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a `Resource`'s id up to limit."""
        visits = Visit.fetch_visited_resource(
            user="",
            resource=arguments.FETCH_VISIT_BY_RESOURCE_ID,
            page=arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT,
            limit=arguments.FETCH_VISIT_WITH_LIMIT,
        )
        self.assertEqual(
            len(visits), arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT_RECORD_COUNT
        )

    @tag("controllers.Visit.fetch_visited_resource_by_user_and_resource")
    def test_fetch_visit_by_user_and_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a username and a `Resource`'s id."""
        visits = Visit.fetch_visited_resource(
            user=arguments.FETCH_VISIT_BY_USER,
            resource=arguments.FETCH_VISIT_BY_RESOURCE_ID,
        )
        self.assertEqual(
            len(visits), arguments.FETCH_VISIT_BY_USER_AND_RESOURCE_RECORD_COUNT
        )
        self.assertEqual(
            visits[0]["visit_count"], arguments.FETCH_VISIT_BY_USER_RECORD_COUNT
        )

    @tag("controllers.Visit.fetch_visited_resource_by_user_dne")
    def test_fetch_visit_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a username where `User` does not exist."""
        visits = Visit.fetch_visited_resource(
            user=arguments.FETCH_VISIT_BY_USER_DNE, resource=None
        )
        self.assertEqual(len(visits), 0)

    @tag("controllers.Visit.fetch_visited_resource_by_resource_dne")
    def test_fetch_visit_by_resource_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a `Resource`'s id where `Resource` does not exist."""
        visits = Visit.fetch_visited_resource(
            user="", resource=arguments.FETCH_VISIT_BY_RESOURCE_ID_DNE
        )
        self.assertEqual(len(visits), 0)
