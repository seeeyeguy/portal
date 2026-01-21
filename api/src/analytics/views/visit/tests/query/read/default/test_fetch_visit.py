"""Collection of pytests for the Visit's fetch view endpoint."""

from typing import List

from django.test import tag
from django.urls import reverse
from rest_framework import status

from portal.models.fixtures import COMMON_FIXTURES
from manager.utils.tests import MultiDBTestCase

# Import constants for expected values
from analytics.controllers.Visit.tests.query.read.default import arguments


@tag(
    "analytics",
    "visit",
    "views",
    "analytics.visit.fetch",
    "visit.fetch.default",
    "views.TestFetchVisit",
)
class TestFetchVisit(MultiDBTestCase):
    """
    Tests for GET /v1/analytics/visits endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Visit/tests/query/read/default/fixtures/resources.json",
        "analytics/controllers/Visit/tests/query/read/default/fixtures/visits.json",
    ]

    url: str = reverse("analytics.visit")

    def setUp(self) -> None:
        super().setUp()
        # Use Django's default test client (same as Query tests)
        pass

    @tag("views.visit.fetch_visit")
    def test_fetch_visit(self) -> None:
        """Success Case: Fetch all `Visit` records."""
        resp = self.client.get(self.url, headers={"content-type": "application/json"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertGreaterEqual(len(data), arguments.FETCH_VISIT_RECORD_COUNT)

        # Structure checks
        self.assertIn("visit_count", data[0])
        self.assertIn("resource", data[0])
        self.assertIn("id", data[0]["resource"])

    @tag("views.visit.fetch_visit_with_page")
    def test_fetch_visit_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records."""
        resp = self.client.get(
            self.url,
            {
                "page": arguments.FETCH_VISIT_WITH_PAGE,
                "limit": arguments.FETCH_VISIT_WITH_LIMIT,
            },
            headers={"content-type": "application/json"},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), arguments.FETCH_VISIT_WITH_PAGE_RECORD_COUNT)

    @tag("views.visit.fetch_visit_with_limit")
    def test_fetch_visit_with_limit(self) -> None:
        """Success Case: Fetch all `Visit` records up to limit."""
        resp = self.client.get(
            self.url,
            {
                "page": 1,
                "limit": arguments.FETCH_VISIT_WITH_LIMIT,
            },
            headers={"content-type": "application/json"},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(resp.json()), arguments.FETCH_VISIT_WITH_LIMIT_RECORD_COUNT
        )

    @tag("views.visit.fetch_visit_by_user")
    def test_fetch_visit_by_user(self) -> None:
        """Success Case: Fetch `Visit` records given a username."""
        resp = self.client.get(
            self.url,
            {"user": arguments.FETCH_VISIT_BY_USER},
            headers={"content-type": "application/json"},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(len(data), arguments.FETCH_VISIT_BY_USER_RECORD_COUNT)

        for row in data:
            self.assertIn("visit_count", row)
            self.assertIn("resource", row)
            self.assertIn("id", row["resource"])

    @tag("views.visit.fetch_visit_by_resource")
    def test_fetch_visit_by_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id."""
        resp = self.client.get(
            self.url,
            {"resource": arguments.FETCH_VISIT_BY_RESOURCE_ID},
            headers={"content-type": "application/json"},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(len(data), arguments.FETCH_VISIT_BY_RESOURCE_RECORD_COUNT)
        self.assertEqual(
            data[0]["resource"]["id"], arguments.FETCH_VISIT_BY_RESOURCE_ID
        )

    @tag("views.visit.fetch_visit_by_user_and_resource")
    def test_fetch_visit_by_user_and_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a username and a `Resource`'s id."""
        params = {
            "user": arguments.FETCH_VISIT_BY_USER,
            "resource": arguments.FETCH_VISIT_BY_RESOURCE_ID,
        }
        resp = self.client.get(
            self.url,
            params,  # type: ignore[arg-type]
            headers={"content-type": "application/json"},
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(
            len(data), arguments.FETCH_VISIT_BY_USER_AND_RESOURCE_RECORD_COUNT
        )
        self.assertIn("visit_count", data[0])
        self.assertEqual(
            data[0]["resource"]["id"], arguments.FETCH_VISIT_BY_RESOURCE_ID
        )

    @tag("views.visit.fetch_visit_by_user_and_resource_with_page")
    def test_fetch_visit_by_user_and_resource_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a username and a `Resource`'s id."""
        params = {
            "user": arguments.FETCH_VISIT_BY_USER,
            "resource": arguments.FETCH_VISIT_BY_RESOURCE_ID,
            "page": arguments.FETCH_VISIT_WITH_PAGE,
            "limit": arguments.FETCH_VISIT_WITH_LIMIT,
        }
        resp = self.client.get(
            self.url,
            params,  # type: ignore[arg-type]
            headers={"content-type": "application/json"},
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(
            len(data), arguments.FETCH_VISIT_WITH_PAGE_AND_LIMIT_RECORD_COUNT
        )
        for row in data:
            self.assertIn("visit_count", row)
            self.assertIn("resource", row)
            self.assertEqual(
                row["resource"]["id"], arguments.FETCH_VISIT_BY_RESOURCE_ID
            )

    @tag("views.visit.fetch_visit_by_user_dne")
    def test_fetch_visit_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a username where `User` does not exist."""
        resp = self.client.get(
            self.url,
            {"user": arguments.FETCH_VISIT_BY_USER_DNE},
            headers={"content-type": "application/json"},
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.visit.fetch_visit_by_resource_dne")
    def test_fetch_visit_by_resource_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a `Resource`'s id where `Resource` does not exist."""
        resp = self.client.get(
            self.url,
            {"resource": arguments.FETCH_VISIT_BY_RESOURCE_ID_DNE},
            headers={"content-type": "application/json"},
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
