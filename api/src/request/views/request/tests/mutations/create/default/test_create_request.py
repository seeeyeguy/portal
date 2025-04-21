"""
Collection of pytests for Request's create view endpoint.
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
    "request_app.request.create",
    "request.create.default",
    "views.TestCreateRequest",
)
class TestCreateRequest(MultiDBTestCase):
    """
    Tests for POST /v1/request/request endpoint.
    """

    def setUp(self) -> None:

        super().setUp()

    fixtures: List[str] = []

    url: str = reverse("request.request")

    @tag("views.request.create_request")
    def test_create_request(self) -> None:
        """Success Case: Create a `Request` record."""

    @tag("views.request.create_request_stage_invalid")
    def test_create_request_stage_invalid(self) -> None:
        """Fail Case: Create a `Request` record with an
        invalid level for stage."""
