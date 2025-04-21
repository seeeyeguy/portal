"""
Collection of pytests for Request's fetch controller.
"""

from typing import List

from django.test import tag

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestFetchRequest",
    "request_app.request.fetch",
    "request.fetch.default",
)
class TestFetchRequest(MultiDBTestCase):
    """Test suite for Request's fetch controller."""

    fixtures: List[str] = []

    @tag("controllers.request.fetch_request")
    def test_fetch_request(self) -> None:
        """Success Case: Fetch a `Request` record."""

    @tag("controllers.request.fetch_requests")
    def test_fetch_requests(self) -> None:
        """Success Case: Fetch all `Request` records."""

    @tag("controllers.request.fetch_requests_with_originator")
    def test_fetch_requests_with_originator(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator."""

    @tag("controllers.request.fetch_requests_with_originator_at_stage")
    def test_fetch_requests_with_originator_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage."""

    @tag("controllers.request.fetch_requests_with_originator_at_stage_with_status")
    def test_fetch_requests_with_originator_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage with the given
        status."""

    @tag("controllers.request.fetch_requests_at_stage")
    def test_fetch_requests_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage."""

    @tag("controllers.request.fetch_requests_at_stage_with_status")
    def test_fetch_requests_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with the given status."""

    @tag("controllers.request.fetch_requests_with_status")
    def test_fetch_requests_with_status(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given status."""

    @tag("controllers.request.fetch_requests_with_page")
    def test_fetch_requests_with_page(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page."""

    @tag("controllers.request.fetch_requests_with_limit")
    def test_fetch_requests_with_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given limit."""

    @tag("controllers.request.fetch_requests_with_page_and_limit")
    def test_fetch_requests_with_page_and_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page and limit."""

    @tag("controllers.request.fetch_requests_include_archived_records")
    def test_fetch_requests_include_archived_records(self) -> None:
        """Success Case: Fetch all `Request` records, including
        historical records for inactive `Resource`s."""

    @tag("controllers.request.fetch_request_request_dne")
    def test_fetch_request_request_dne(self) -> None:
        """Fail Case: Fetch a `Request` record where the record
        does not exist for the given id."""

    @tag("controllers.request.fetch_requests_originator_dne")
    def test_fetch_requests_originator_dne(self) -> None:
        """Fail Case: Fetch `Request` records where a `User`
        does not exist for the given originator."""

    @tag("controllers.request.fetch_requests_originator_access_dne")
    def test_fetch_requests_originator_access_dne(self) -> None:
        """Fail Case: Fetch `Request` records where an appropriate
        `Access` does not exist for the given originator."""
