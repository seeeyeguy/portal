"""Collection of pytests for the Visit's fetch view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "analytics",
    "visit",
    "views",
    "analytics.visit.fetch",
    "visit.fetch.default",
    "views.TestFetchVisit",
)
class TestFetchVisit(TestCase):
    """
    Tests for GET /v1/analytics/visits endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/tags/tags.json",
        "portal/models/fixtures/stages/stages.json",
        "portal/models/fixtures/users/users.json",
        "portal/models/fixtures/roles/roles.json",
        "portal/models/fixtures/accesses/accesses.json",
    ]

    url: str = reverse("analytics.visit")

    @tag("views.visit.fetch_visit")
    def test_fetch_visit(self) -> None:
        """Success Case: Fetch all `Visit` records."""

    @tag("views.visit.fetch_visit_with_page")
    def test_fetch_visit_with_page(self) -> None:
        """Success Case: Fetch page of `Visit` records."""

    @tag("views.visit.fetch_visit_with_limit")
    def test_fetch_visit_with_limit(self) -> None:
        """Success Case: Fetch all `Visit` records up to limit."""

    @tag("views.visit.fetch_visit_with_page_and_limit")
    def test_fetch_visit_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Visit` records up to limit."""

    @tag("views.visit.fetch_visit_by_id")
    def test_fetch_visit_by_id(self) -> None:
        """Success Case: Fetch a `Visit` record given an id."""

    @tag("views.visit.fetch_visit_by_user")
    def test_fetch_visit_by_user(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email."""

    @tag("views.visit.fetch_visit_by_user_with_page")
    def test_fetch_visit_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email."""

    @tag("views.visit.fetch_visit_by_user_with_limit")
    def test_fetch_visit_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email
        up to limit."""

    @tag("views.visit.fetch_visit_by_user_with_page_and_limit")
    def test_fetch_visit_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email up to limit."""

    @tag("views.visit.fetch_visit_by_resource")
    def test_fetch_visit_by_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id."""

    @tag("views.visit.fetch_visit_by_resource_with_page")
    def test_fetch_visit_by_resource_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        `Resource`'s id."""

    @tag("views.visit.fetch_visit_by_resource_with_limit")
    def test_fetch_visit_by_resource_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id
        up to limit."""

    @tag("views.visit.fetch_visit_by_resource_with_page_and_limit")
    def test_fetch_visit_by_resource_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        `Resource`'s id up to limit."""

    @tag("views.visit.fetch_visit_by_user_and_resource")
    def test_fetch_visit_by_user_and_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email
        and a `Resource`'s id."""

    @tag("views.visit.fetch_visit_by_user_and_resource_with_page")
    def test_fetch_visit_by_user_and_resource_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email and a `Resource`'s id."""

    @tag("views.visit.fetch_visit_by_user_and_resource_with_limit")
    def test_fetch_visit_by_user_and_resource_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email and
        a `Resource`'s id up to limit."""

    @tag("views.visit.fetch_visit_by_user_and_resource_with_page_and_limit")
    def test_fetch_visit_by_user_and_resource_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email and a `Resource`'s id up to limit."""

    @tag("views.visit.fetch_visit_by_id_dne")
    def test_fetch_visit_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given an id where record
        does not exist."""

    @tag("views.visit.fetch_visit_by_user_dne")
    def test_fetch_visit_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a user's email
        where `User` does not exist."""

    @tag("views.visit.fetch_visit_by_resource_dne")
    def test_fetch_visit_by_resource_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a `Resource`'s id
        where `Resource` does not exist."""
