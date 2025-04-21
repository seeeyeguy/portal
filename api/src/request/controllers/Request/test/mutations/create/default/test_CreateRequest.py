"""
Collection of pytests for Request's create controller.
"""

from typing import List

from django.test import tag

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestCreateRequest",
    "request_app.request.create",
    "request.create.default",
)
class TestCreateRequest(MultiDBTestCase):
    """Test suite for Request's create controller."""

    fixtures: List[str] = []

    @tag("controllers.request.create_request")
    def test_create_request(self) -> None:
        """Success Case: Create a `Request` record."""

    @tag("controllers.request.create_request_stage_invalid")
    def test_create_request_stage_invalid(self) -> None:
        """Fail Case: Create a `Request` record with an
        invalid level for stage."""
