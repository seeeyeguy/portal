"""
Collection of pytests for Resource's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "directory",
    "resource",
    "views",
    "directory.resource.fetch",
    "resource.fetch.default",
    "views.TestFetchResources",
)
class TestFetchResource(TestCase):
    """
    Tests for GET /v1/directory/resources endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
    ]

    url: str = reverse("directory.resource")

    @tag("views.resource.fetch_resources")
    def test_fetch_resources(self) -> None:
        """Success Case: Fetch all `Resource` records."""

    @tag("views.resource.fetch_resources_with_page")
    def test_fetch_resources_with_page(self) -> None:
        """Success Case: Fetch page of `Resource` records."""

    @tag("views.resource.fetch_resources_with_limit")
    def test_fetch_resources_with_limit(self) -> None:
        """Success Case: Fetch all `Resource` records up to limit."""

    @tag("views.resource.fetch_resources_with_page_and_limit")
    def test_fetch_resources_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Resource` records up to limit."""

    @tag("views.resource.fetch_resources_with_page_exceeding_page_count")
    def test_fetch_resources_with_page_exceeding_page_count(self) -> None:
        """Success Case: Fetch page of `Resource` records using a
        page number that exceeds the number of pages."""

    @tag("views.resource.fetch_resource_by_id")
    def test_fetch_resource_by_id(self) -> None:
        """Success Case: Fetch a `Resource` record given an id."""

    @tag("views.resource.fetch_resource_by_id_dne")
    def test_fetch_resource_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        record does not exist."""

    @tag("views.resource.fetch_resource_by_id_with_page")
    def test_fetch_resource_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a page is also supplied in the parameters."""

    @tag("views.resource.fetch_resource_by_id_with_limit")
    def test_fetch_resource_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a limit is also supplied in the parameters."""

    @tag("views.resource.fetch_resource_by_id_with_page_and_limit")
    def test_fetch_resource_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a page and limit is also supplied in the parameters."""
