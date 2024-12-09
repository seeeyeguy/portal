"""
Collection of pytests for Resource's update view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "directory",
    "resource",
    "views",
    "directory.resource.update",
    "resource.update.default",
    "views.TestUpdateResource",
)
class TestUpdateResource(TestCase):
    """
    Tests for PUT /v1/directory/resources endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
    ]

    url: str = reverse("directory.resource")

    @tag("views.resource.update_resource")
    def test_update_resource(self) -> None:
        """Success Case: Update a `Resource` record."""

    @tag("views.resource.update_resource_record_dne")
    def test_update_resource_record_dne(self) -> None:
        """Fail Case: Update a `Resource` that does not exist."""

    @tag("views.resource.update_resource_approved_resource")
    def test_update_resource_approved_resource(self) -> None:
        """Fail Case: Update a `Resource` record that has a revision number
        which indicates it has been approved."""

    @tag("views.resource.update_resource_invalid_url")
    def test_update_resource_invalid_url(self) -> None:
        """Fail Case: Update a `Resource` record with a malformed url."""

    @tag("views.resource.update_resource_url_not_found")
    def test_update_resource_url_not_found(self) -> None:
        """Fail Case: Update a `Resource` record with a url that returns a 404
        response."""

    @tag("views.resource.update_resource_invalid_thumbnail")
    def test_update_resource_invalid_thumbnail(self) -> None:
        """Fail Case: Update a `Resource` record with an invalid thumbnail."""

    @tag("views.resource.update_resource_employee_level_dne")
    def test_update_resource_employee_level_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given employee level id
        where that `EmployeeLevel` does not exist."""

    @tag("views.resource.update_resource_subfunction_dne")
    def test_update_resource_subfunction_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given subfunction id
        where that `SubFunction` does not exist."""

    @tag("views.resource.update_resource_tag_dne")
    def test_update_resource_tag_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given tag id
        where that `Tag` does not exist."""
