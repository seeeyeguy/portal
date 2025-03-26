"""
Collection of pytests for Resource's update view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Resource.tests.mutations.update.default import arguments

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

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.UPDATE_RESOURCE_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/dispositions.json",
    ]

    url: str = reverse("directory.resource")

    @tag("views.resource.update_resource")
    def test_update_resource(self) -> None:
        """Success Case: Update a `Resource` record."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data=arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
            content_type="application/json",
        )

        resource = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictEqual(resource, arguments.VALID_UPDATED_RESOURCE)

    @tag("views.resource.update_resource_record_dne")
    def test_update_resource_record_dne(self) -> None:
        """Fail Case: Update a `Resource` that does not exist."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_DNE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data=arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.update_resource_with_duplicate_pending_draft")
    def test_update_resource_with_duplicate_pending_draft(self) -> None:
        """Fail Case: Update a `Resource` that has a duplicate pending draft."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_WITH_DUPLICATE_PENDING_DRAFT_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data=arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_approved_resource")
    def test_update_resource_approved_resource(self) -> None:
        """Fail Case: Update a `Resource` record that has a revision number
        which indicates it has been approved."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_APPROVED_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data=arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_duplicate_name")
    def test_update_resource_duplicate_name(self) -> None:
        """Fail Case: Update a `Resource` record with a duplicate name
        of another active `Resource`."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "name": arguments.UPDATE_RESOURCE_DUPLICATE_RESOURCE_NAME,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_invalid_description")
    def test_update_resource_invalid_description(self) -> None:
        """Fail Case: Update a `Resource` record with an invalid
        description."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "description": arguments.UPDATE_RESOURCE_INVALID_RESOURCE_DESCRIPTION,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_invalid_url")
    def test_update_resource_invalid_url(self) -> None:
        """Fail Case: Update a `Resource` record with a malformed url."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "url": arguments.UPDATE_RESOURCE_MALFORMED_RESOURCE_URL,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_invalid_thumbnail")
    def test_update_resource_invalid_thumbnail(self) -> None:
        """Fail Case: Update a `Resource` record with an invalid thumbnail."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "thumbnail": arguments.UPDATE_RESOURCE_INVALID_RESOURCE_THUMBNAIL,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_empty_employee_levels")
    def test_update_resource_employee_level_empty_employee_levels(self) -> None:
        """Fail Case: Update a `Resource` record without supplying employee
        level ids."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "employee_levels": [],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_employee_level_dne")
    def test_update_resource_employee_level_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given employee level id
        where that `EmployeeLevel` does not exist."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "employee_levels": arguments.UPDATE_RESOURCE_EMPLOYEE_LEVEL_DNE_IDS,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.update_resource_empty_subfunctions")
    def test_update_resource_employee_level_empty_subfunctions(self) -> None:
        """Fail Case: Update a `Resource` record without supplying
        subfunction ids."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "subfunctions": [],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.update_resource_subfunction_dne")
    def test_update_resource_subfunction_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given subfunction id
        where that `SubFunction` does not exist."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "subfunctions": arguments.UPDATE_RESOURCE_SUBFUNCTION_DNE_IDS,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.update_resource_tag_dne")
    def test_update_resource_tag_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given tag id
        where that `Tag` does not exist."""

        request_url = f"{self.url}?id={arguments.UPDATE_RESOURCE_ID}"

        response = self.client.put(
            request_url,
            data={
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "tags": arguments.UPDATE_RESOURCE_TAG_DNE_IDS,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
