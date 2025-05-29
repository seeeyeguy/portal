"""
Collection of pytests for Resource's create view endpoint.
"""

from typing import List
from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.Resource.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "resource",
    "views",
    "directory.resource.create",
    "resource.create.default",
    "views.TestCreateResource",
)
class TestCreateResource(MultiDBTestCase):
    """
    Tests for POST /v1/directory/resources endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.CREATE_RESOURCE_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/users.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/roles.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/accesses.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/pointofcontacts.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    url: str = reverse("directory.resource")

    @tag("views.resource.create_resource")
    def test_create_resource(self) -> None:
        """Success Case: Create a `Resource` record."""

        response = self.client.post(
            self.url,
            data=arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
            content_type="application/json",
        )

        resource = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del resource["created"]
        del resource["uid"]

        self.assertDictEqual(resource, arguments.VALID_CREATED_RESOURCE)

    @tag("views.resource.create_resource_revision")
    def test_create_resource_revision(self) -> None:
        """Success Case: Create a `Resource` record revision."""

        response = self.client.post(
            self.url,
            data=arguments.BASE_CREATE_RESOURCE_REVISION_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
            content_type="application/json",
        )

        resource = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del resource["created"]

        self.assertDictEqual(resource, arguments.VALID_CREATED_RESOURCE_REVISION)

    @tag("views.resource.create_resource_previous_revision_dne")
    def test_create_resource_previous_revision_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given previous revision
        id where that `Resource` does not exist."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "previous_revision": arguments.CREATE_RESOURCE_PREVIOUS_RESOURCE_REVISION_DNE_ID,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.create_resource_revision_erroneous_previous_revision")
    def test_create_resource_revision_erroneous_previous_revision(self) -> None:
        """Fail Case: Create a `Resource` record revision for a resource with a
        different `Resource.uid`."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "previous_revision": 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_with_duplicate_pending_draft")
    def test_create_resource_with_duplicate_pending_draft(self) -> None:
        """Fail Case: Create a `Resource` that has a duplicate pending draft."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "uid": arguments.CREATE_RESOURCE_WITH_DUPLICATE_PENDING_DRAFT_RESOURCE_ID,
                "previous_revision": arguments.CREATE_RESOURCE_PREVIOUS_RESOURCE_REVISION_ID,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_duplicate_name")
    def test_create_resource_duplicate_name(self) -> None:
        """Fail Case: Create a `Resource` record with a duplicate name
        of another active `Resource`."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "name": arguments.CREATE_RESOURCE_DUPLICATE_RESOURCE_NAME,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_invalid_description")
    def test_create_resource_invalid_description(self) -> None:
        """Fail Case: Create a `Resource` record with an invalid
        description."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "description": arguments.CREATE_RESOURCE_INVALID_RESOURCE_DESCRIPTION,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_malformed_url")
    def test_create_resource_malformed_url(self) -> None:
        """Fail Case: Create a `Resource` record with a malformed url."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "url": arguments.CREATE_RESOURCE_MALFORMED_RESOURCE_URL,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_empty_employee_levels")
    def test_create_resource_empty_employee_levels(self) -> None:
        """Fail Case: Create a `Resource` record without supplying
        employee level ids."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "employee_levels": [],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_employee_level_dne")
    def test_create_resource_employee_level_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given employee level id
        where that `EmployeeLevel` does not exist."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "employee_levels": arguments.CREATE_RESOURCE_EMPLOYEE_LEVEL_DNE_IDS,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.create_resource_empty_subfunctions")
    def test_create_resource_empty_subfunctions(self) -> None:
        """Fail Case: Create a `Resource` record without supplying
        subfunction ids."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "subfunctions": [],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_subfunction_dne")
    def test_create_resource_subfunction_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given subfunction id
        where that `SubFunction` does not exist."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "subfunctions": arguments.CREATE_RESOURCE_SUBFUNCTION_DNE_IDS,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.create_resource_subfunctions_permissions_denied")
    def test_create_resource_subfunctions_permissions_denied(self) -> None:
        """Fail Case: Create a `Resource` record where the `User` does not have
        permissions to create a `Resource` within the given `SubFunction`s."""

        user = AuthModels.User.objects.get(
            email=arguments.CREATE_RESOURCE_USER_EMAIL_SUBFUNCTIONS_PERMISSIONS_DENIED
        )
        self.client.force_login(user=user)

        response = self.client.post(
            self.url,
            data=arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.resource.create_resource_tag_dne")
    def test_create_resource_tag_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given tag id
        where that `Tag` does not exist."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "tags": arguments.CREATE_RESOURCE_TAG_DNE_IDS,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.create_resource_empty_point_of_contacts")
    def test_create_resource_empty_point_of_contacts(self) -> None:
        """Fail Case: Create a `Resource` record without supplying emails
        for point of contacts."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "point_of_contacts": [],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_point_of_contact_dne")
    def test_create_resource_point_of_contact_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given `User` email for
        a point of contact where an appropriate `User` for that `PointOfContact`
        does not exist."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "point_of_contacts": arguments.CREATE_RESOURCE_POINT_OF_CONTACT_EMAILS_DNE,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.create_resource_invalid_thumbnail")
    def test_create_resource_invalid_thumbnail(self) -> None:
        """Fail Case: Create a `Resource` record with an invalid thumbnail."""

        response = self.client.post(
            self.url,
            data={
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
                "thumbnail": arguments.CREATE_RESOURCE_INVALID_RESOURCE_THUMBNAIL,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.create_resource_invalid_user_role")
    def test_create_resource_invalid_user_role(self) -> None:
        """Fail Case: Create a `Resource` record with a `User` that
        has an invalid `Role`."""

        user_with_invalid_role = AuthModels.User.objects.get(
            email=arguments.CREATE_RESOURCE_USER_EMAIL_INVALID_ROLE
        )
        self.client.force_login(user_with_invalid_role)

        response = self.client.post(
            self.url,
            data=arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
