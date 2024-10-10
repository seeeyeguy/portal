"""
Collection of pytests for Visit's fetch controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "analytics",
    "visit",
    "controllers.TestFetchVisit",
    "analytics.visit.fetch",
    "visit.fetch.default",
)
class TestFetchVisit(TestCase):
    """Test suite for Visit's fetch controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.visit.fetch_visit")
    def test_fetch_visit(self) -> None:
        """Success Case: Fetch all `Visit` records."""

    @tag("controllers.visit.fetch_visit_with_page")
    def test_fetch_visit_with_page(self) -> None:
        """Success Case: Fetch page of `Visit` records."""

    @tag("controllers.visit.fetch_visit_with_limit")
    def test_fetch_visit_with_limit(self) -> None:
        """Success Case: Fetch all `Visit` records up to limit."""

    @tag("controllers.visit.fetch_visit_with_page_and_limit")
    def test_fetch_visit_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Visit` records up to limit."""

    @tag("controllers.visit.fetch_visit_by_id")
    def test_fetch_visit_by_id(self) -> None:
        """Success Case: Fetch a `Visit` record given an id."""

    @tag("controllers.visit.fetch_visit_by_user")
    def test_fetch_visit_by_user(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email."""

    @tag("controllers.visit.fetch_visit_by_user_with_page")
    def test_fetch_visit_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email."""

    @tag("controllers.visit.fetch_visit_by_user_with_limit")
    def test_fetch_visit_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email
        up to limit."""

    @tag("controllers.visit.fetch_visit_by_user_with_page_and_limit")
    def test_fetch_visit_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email up to limit."""

    @tag("controllers.visit.fetch_visit_by_resource")
    def test_fetch_visit_by_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id."""

    @tag("controllers.visit.fetch_visit_by_resource_with_page")
    def test_fetch_visit_by_resource_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        `Resource`'s id."""

    @tag("controllers.visit.fetch_visit_by_resource_with_limit")
    def test_fetch_visit_by_resource_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a `Resource`'s id
        up to limit."""

    @tag("controllers.visit.fetch_visit_by_resource_with_page_and_limit")
    def test_fetch_visit_by_resource_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        `Resource`'s id up to limit."""

    @tag("controllers.visit.fetch_visit_by_user_and_resource")
    def test_fetch_visit_by_user_and_resource(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email
        and a `Resource`'s id."""

    @tag("controllers.visit.fetch_visit_by_user_and_resource_with_page")
    def test_fetch_visit_by_user_and_resource_with_page(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email and a `Resource`'s id."""

    @tag("controllers.visit.fetch_visit_by_user_and_resource_with_limit")
    def test_fetch_visit_by_user_and_resource_with_limit(self) -> None:
        """Success Case: Fetch `Visit` records given a user's email and
        a `Resource`'s id up to limit."""

    @tag("controllers.visit.fetch_visit_by_user_and_resource_with_page_and_limit")
    def test_fetch_visit_by_user_and_resource_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Visit` records given a
        user's email and a `Resource`'s id up to limit."""

    @tag("controllers.visit.fetch_visit_by_id_dne")
    def test_fetch_visit_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given an id where record
        does not exist."""

    @tag("controllers.visit.fetch_visit_by_user_dne")
    def test_fetch_visit_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a user's email
        where `User` does not exist."""

    @tag("controllers.visit.fetch_visit_by_resource_dne")
    def test_fetch_visit_by_resource_dne(self) -> None:
        """Fail Case: Fetch a `Visit` record given a `Resource`'s id
        where `Resource` does not exist."""
