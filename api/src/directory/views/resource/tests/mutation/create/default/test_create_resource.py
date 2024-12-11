"""
Collection of pytests for Resource's create view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "directory",
    "resource",
    "views",
    "directory.resource.create",
    "resource.create.default",
    "views.TestCreateResource",
)
class TestCreateResource(TestCase):
    """
    Tests for POST /v1/directory/resources endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
    ]

    url: str = reverse("directory.resource")

    @tag("views.resource.create_resource")
    def test_create_resource(self) -> None:
        """Success Case: Create a `Resource` record."""

    @tag("views.resource.create_resource_previous_revision_dne")
    def test_create_resource_previous_revision_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given previous revision
        id where that `Resource` does no exist."""

    @tag("views.resource.create_resource_invalid_url")
    def test_create_resource_invalid_url(self) -> None:
        """Fail Case: Create a `Resource` record with a malformed url."""

    @tag("views.resource.create_resource_url_not_found")
    def test_create_resource_url_not_found(self) -> None:
        """Fail Case: Create a `Resource` record with a url that returns a 404
        response."""

    @tag("views.resource.create_resource_invalid_thumbnail")
    def test_create_resource_invalid_thumbnail(self) -> None:
        """Fail Case: Create a `Resource` record with an invalid thumbnail."""

    @tag("views.resource.create_resource_employee_level_dne")
    def test_create_resource_employee_level_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given employee level id
        where that `EmployeeLevel` does not exist."""

    @tag("views.resource.create_resource_subfunction_dne")
    def test_create_resource_subfunction_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given subfunction id
        where that `SubFunction` does not exist."""

    @tag("views.resource.create_resource_tag_dne")
    def test_create_resource_tag_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given tag id
        where that `Tag` does not exist."""
