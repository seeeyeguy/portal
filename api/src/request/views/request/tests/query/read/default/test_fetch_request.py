"""
Collection of pytests for Request's fetch view endpoint.
"""

from typing import List

# NEED TO REMOVE pylint-disable AFTER IMPLEMENTATION.
# pylint: disable=useless-parent-delegation
from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "request_app",
    "request",
    "views",
    "request_app.request.fetch",
    "request.fetch.default",
    "views.TestFetchRequest",
)
class TestFetchRequest(MultiDBTestCase):
    """
    Tests for GET /v1/request/request endpoint.
    """

    def setUp(self) -> None:

        super().setUp()

    fixtures: List[str] = []

    url: str = reverse("request.request")

    @tag("views.request.fetch_request")
    def test_fetch_request(self) -> None:
        """Success Case: Fetch a `Request` record."""

    @tag("views.request.fetch_requests")
    def test_fetch_requests(self) -> None:
        """Success Case: Fetch all `Request` records."""

    @tag("views.request.fetch_requests_with_originator")
    def test_fetch_requests_with_originator(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator."""

    @tag("views.request.fetch_requests_with_originator_at_stage")
    def test_fetch_requests_with_originator_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage."""

    @tag("views.request.fetch_requests_with_originator_at_stage_with_status")
    def test_fetch_requests_with_originator_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage with the given
        status."""

    @tag("views.request.fetch_requests_at_stage")
    def test_fetch_requests_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage."""

    @tag("views.request.fetch_requests_at_stage_with_status")
    def test_fetch_requests_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with the given status."""

    @tag("views.request.fetch_requests_with_status")
    def test_fetch_requests_with_status(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given status."""

    @tag("views.request.fetch_requests_with_page")
    def test_fetch_requests_with_page(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page."""

    @tag("views.request.fetch_requests_with_limit")
    def test_fetch_requests_with_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given limit."""

    @tag("views.request.fetch_requests_with_page_and_limit")
    def test_fetch_requests_with_page_and_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page and limit."""

    @tag("views.request.fetch_requests_include_archived_records")
    def test_fetch_requests_include_archived_records(self) -> None:
        """Success Case: Fetch all `Request` records, including
        historical records for inactive `Resource`s."""

    @tag("views.request.fetch_request_request_dne")
    def test_fetch_request_request_dne(self) -> None:
        """Fail Case: Fetch a `Request` record where the record
        does not exist for the given id."""

    @tag("views.request.fetch_requests_originator_dne")
    def test_fetch_requests_originator_dne(self) -> None:
        """Fail Case: Fetch `Request` records where a `User`
        does not exist for the given originator."""

    @tag("views.request.fetch_requests_originator_access_dne")
    def test_fetch_requests_originator_access_dne(self) -> None:
        """Fail Case: Fetch `Request` records where an appropriate
        `Access` does not exist for the given originator."""
