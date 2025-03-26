"""
Collection of pytests for Resource's create controller.
"""

import pytest
from typing import List

from django.test import tag, TestCase

from directory.controllers.Resource.Resource import CreateResourceParams, Resource
from directory.controllers.Resource.tests.mutations.create.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Resource import Resource as ResourceModel
from directory.models.Resource.serializers import ResourceSerializer

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "directory",
    "resource",
    "controllers.TestCreateResource",
    "directory.resource.create",
    "resource.create.default",
)
class TestCreateResource(TestCase):
    """Test suite for Resource's create controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    @tag("controllers.resource.create_resource")
    def test_create_resource(self) -> None:
        """Success Case: Create a `Resource` record."""

        resource = Resource.create_resource(
            arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS
        )

        self.assertIsInstance(resource, ResourceModel)

        # Serialize `Resource`.
        serialized_resource: dict = ResourceSerializer(resource).data

        # Remove dynamic datetime field and uid before comparison.
        del serialized_resource["created"]
        del serialized_resource["uid"]

        self.assertEqual(serialized_resource, arguments.VALID_CREATED_RESOURCE)

    @tag("controllers.resource.create_resource_revision")
    def test_create_resource_revision(self) -> None:
        """Success Case: Create a `Resource` record revision."""

        resource = Resource.create_resource(
            arguments.BASE_CREATE_RESOURCE_REVISION_STRUCTURE_PARAMS
        )

        self.assertIsInstance(resource, ResourceModel)

        # Serialize `Resource`.
        serialized_resource: dict = ResourceSerializer(resource).data

        # Remove dynamic datetime field before comparison.
        del serialized_resource["created"]

        self.assertEqual(serialized_resource, arguments.VALID_CREATED_RESOURCE_REVISION)

    @tag("controllers.resource.create_resource_previous_revision_dne")
    def test_create_resource_previous_revision_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given previous revision
        id where that `Resource` does not exist."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "previous_revision": arguments.CREATE_RESOURCE_PREVIOUS_RESOURCE_REVISION_DNE_ID,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_revision_erroneous_previous_revision")
    def test_create_resource_revision_erroneous_previous_revision(self) -> None:
        """Fail Case: Create a `Resource` record revision for a resource with a
        different `Resource.uid`."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "previous_revision": 1,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_with_duplicate_pending_draft")
    def test_create_resource_with_duplicate_pending_draft(self) -> None:
        """Fail Case: Create a `Resource` record that has a duplicate pending draft."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "uid": arguments.CREATE_RESOURCE_WITH_DUPLICATE_PENDING_DRAFT_RESOURCE_ID,
                "previous_revision": arguments.CREATE_RESOURCE_PREVIOUS_RESOURCE_REVISION_ID,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_duplicate_name")
    def test_create_resource_duplicate_name(self) -> None:
        """Fail Case: Create a `Resource` record with a duplicate name
        of another active `Resource`."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "name": arguments.CREATE_RESOURCE_DUPLICATE_RESOURCE_NAME,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_invalid_description")
    def test_create_resource_invalid_description(self) -> None:
        """Fail Case: Create a `Resource` record with an invalid
        description."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "description": arguments.CREATE_RESOURCE_INVALID_RESOURCE_DESCRIPTION,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_invalid_resource_url")
    def test_create_resource_invalid_resource_url(self) -> None:
        """Fail Case: Create a `Resource` record with a malformed url."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "url": arguments.CREATE_RESOURCE_MALFORMED_RESOURCE_URL,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_empty_employee_levels")
    def test_create_resource_empty_employee_levels(self) -> None:
        """Fail Case: Create a `Resource` record without supplying
        employee level ids."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "employee_levels": [],
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_employee_level_dne")
    def test_create_resource_employee_level_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given employee level id
        where that `EmployeeLevel` does not exist."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "employee_levels": arguments.CREATE_RESOURCE_EMPLOYEE_LEVEL_DNE_IDS,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_empty_subfunctions")
    def test_create_resource_empty_subfunctions(self) -> None:
        """Fail Case: Create a `Resource` record without supplying
        subfunction ids."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "subfunctions": [],
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_subfunction_dne")
    def test_create_resource_subfunction_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given subfunction id
        where that `SubFunction` does not exist."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "subfunctions": arguments.CREATE_RESOURCE_SUBFUNCTION_DNE_IDS,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_tag_dne")
    def test_create_resource_tag_dne(self) -> None:
        """Fail Case: Create a `Resource` record with a given tag id
        where that `Tag` does not exist."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "tags": arguments.CREATE_RESOURCE_TAG_DNE_IDS,
            }

            _ = Resource.create_resource(params)

    @tag("controllers.resource.create_resource_invalid_resource_thumbnail")
    def test_create_resource_invalid_resource_thumbnail(self) -> None:
        """Fail Case: Create a `Resource` record with an invalid thumbnail."""

        with pytest.raises(DirectoryError):
            params: CreateResourceParams = {
                **arguments.BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
                "thumbnail": arguments.CREATE_RESOURCE_INVALID_RESOURCE_THUMBNAIL,  # type: ignore[typeddict-item,unused-ignore]
            }

            _ = Resource.create_resource(params)
