"""
Collection of pytests for Request's update view endpoint.
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
    "request_app.request.update",
    "request.update.default",
    "views.TestUpdateRequest",
)
class TestUpdateRequest(MultiDBTestCase):
    """
    Tests for PUT /v1/request/request endpoint.
    """

    def setUp(self) -> None:

        super().setUp()

    fixtures: List[str] = []

    url: str = reverse("request.request")

    @tag("views.request.update_request")
    def test_update_request(self) -> None:
        """Success Case: Update a `Request` record."""

    @tag("views.request.update_request_request_dne")
    def test_update_request_request_dne(self) -> None:
        """Fail Case: Update a `Request` record where
        the record does not exist for the given id."""

    @tag("views.request.update_request_stage_invalid")
    def test_update_request_stage_invalid(self) -> None:
        """Fail Case: Update a `Request` record with an
        invalid level for stage."""
