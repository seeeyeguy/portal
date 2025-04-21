"""
Collection of pytests for Request's update controller.
"""

from typing import List

from django.test import tag

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestUpdateRequest",
    "request_app.request.update",
    "request.update.default",
)
class TestUpdateRequest(MultiDBTestCase):
    """Test suite for Request's update controller."""

    fixtures: List[str] = []

    @tag("controllers.request.update_request")
    def test_update_request(self) -> None:
        """Success Case: Update a `Request` record."""

    @tag("controllers.request.update_request_request_dne")
    def test_update_request_request_dne(self) -> None:
        """Fail Case: Update a `Request` record where
        the record does not exist for the given id."""

    @tag("controllers.request.update_request_stage_invalid")
    def test_update_request_stage_invalid(self) -> None:
        """Fail Case: Update a `Request` record with an
        invalid level for stage."""
