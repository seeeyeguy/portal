"""
Collection of pytests for Resource's update controller.
"""

import pytest
from typing import List

from django.test import tag, TestCase

from directory.controllers.Resource.Resource import Resource, UpdateResourceParams
from directory.controllers.Resource.tests.mutations.update.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Resource.Resource import Resource as ResourceModel
from directory.models.Resource.serializers import ResourceSerializer

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "directory",
    "resource",
    "controllers.TestUpdateResource",
    "directory.resource.update",
    "resource.update.default",
)
class TestUpdateResource(TestCase):
    """Test suite for Resource's update controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/mutations/update/default/fixtures/dispositions.json",
    ]

    @tag("controllers.resource.update_resource")
    def test_update_resource(self) -> None:
        """Success Case: Update a `Resource` record."""

        resource, rows_affected = Resource.update_resource(
            arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS
        )

        self.assertIsInstance(resource, ResourceModel)
        self.assertEqual(
            rows_affected, arguments.UPDATE_RESOURCE_EXPECTED_AFFECTED_ROWS
        )

        # Serialize `Resource`.
        serialized_resource: dict = ResourceSerializer(resource).data
        self.assertDictEqual(serialized_resource, arguments.VALID_UPDATED_RESOURCE)

    @tag("controllers.resource.update_resource_record_dne")
    def test_update_resource_record_dne(self) -> None:
        """Fail Case: Update a `Resource` that does not exist."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "resource_id": arguments.UPDATE_RESOURCE_DNE_RESOURCE_ID,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_with_duplicate_pending_draft")
    def test_update_resource_with_duplicate_pending_draft(self) -> None:
        """Fail Case: Update a `Resource` that has a duplicate pending draft."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "resource_id": arguments.UPDATE_RESOURCE_WITH_DUPLICATE_PENDING_DRAFT_RESOURCE_ID,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_approved_resource")
    def test_update_resource_approved_resource(self) -> None:
        """Fail Case: Update a `Resource` record that has a revision number
        which indicates it has been approved."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "resource_id": arguments.UPDATE_RESOURCE_APPROVED_RESOURCE_ID,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_duplicate_name")
    def test_update_resource_duplicate_name(self) -> None:
        """Fail Case: Update a `Resource` record with a duplicate name
        of another active `Resource`."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "name": arguments.UPDATE_RESOURCE_DUPLICATE_RESOURCE_NAME,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_invalid_description")
    def test_update_resource_invalid_description(self) -> None:
        """Fail Case: Update a `Resource` record with an invalid
        description."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "description": arguments.UPDATE_RESOURCE_INVALID_RESOURCE_DESCRIPTION,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_invalid_url")
    def test_update_resource_invalid_url(self) -> None:
        """Fail Case: Update a `Resource` record with a malformed url."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "url": arguments.UPDATE_RESOURCE_MALFORMED_RESOURCE_URL,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_invalid_thumbnail")
    def test_update_resource_invalid_thumbnail(self) -> None:
        """Fail Case: Update a `Resource` record with an invalid thumbnail."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "thumbnail": arguments.UPDATE_RESOURCE_INVALID_RESOURCE_THUMBNAIL,  # type: ignore[typeddict-item,unused-ignore]
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_empty_employee_levels")
    def test_update_resource_employee_level_empty_employee_levels(self) -> None:
        """Fail Case: Update a `Resource` record without supplying employee
        level ids."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "employee_levels": [],
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_employee_level_dne")
    def test_update_resource_employee_level_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given employee level id
        where that `EmployeeLevel` does not exist."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "employee_levels": arguments.UPDATE_RESOURCE_EMPLOYEE_LEVEL_DNE_IDS,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_empty_subfunctions")
    def test_update_resource_employee_level_empty_subfunctions(self) -> None:
        """Fail Case: Update a `Resource` record without supplying
        subfunction ids."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "subfunctions": [],
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_subfunction_dne")
    def test_update_resource_subfunction_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given subfunction id
        where that `SubFunction` does not exist."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "subfunctions": arguments.UPDATE_RESOURCE_SUBFUNCTION_DNE_IDS,
            }
            _, _ = Resource.update_resource(params)

    @tag("controllers.resource.update_resource_tag_dne")
    def test_update_resource_tag_dne(self) -> None:
        """Fail Case: Update a `Resource` record with a given tag id
        where that `Tag` does not exist."""

        with pytest.raises(DirectoryError):
            params: UpdateResourceParams = {
                **arguments.BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS,
                "tags": arguments.UPDATE_RESOURCE_TAG_DNE_IDS,
            }
            _, _ = Resource.update_resource(params)
