"""
Collection of pytests for SubFunction's update controller.
"""

import pytest
from typing import List

from django.test import tag

from directory.controllers import SubFunction
from directory.controllers.SubFunction.tests.mutations.update.default import arguments
from directory.exceptions import DirectoryError
from directory.models import SubFunction as SubFunctionModel
from directory.models.SubFunction.serializers import SubFunctionSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestUpdateSubFunction",
    "directory.subfunction.update",
    "subfunction.update.default",
)
class TestUpdateSubFunction(MultiDBTestCase):
    """Test suite for SubFunction's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.update_subfunction")
    def test_update_subfunction(self) -> None:
        """Success Case: Update a `SubFunction` record."""

        subfunction, rows_affected = SubFunction.update_subfunction(
            subfunction_id=arguments.UPDATE_SUBFUNCTION_ID,
            name=arguments.UPDATE_SUBFUNCTION_NAME,
            description=arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
            function=arguments.UPDATE_SUBFUNCTION_FUNCTION_ID,
        )

        self.assertIsInstance(subfunction, SubFunctionModel)

        self.assertEqual(
            rows_affected, arguments.UPDATE_SUBFUNCTION_EXPECTED_ROWS_AFFECTED
        )

        # Serialize `SubFunction` instance.
        serialized_subfunction: dict = SubFunctionSerializer(subfunction).data

        # Remove dynamic datetime field before comparison.
        del serialized_subfunction["modified"]

        self.assertDictEqual(serialized_subfunction, arguments.VALID_SUBFUNCTION)

    @tag("controllers.subfunction.update_subfunction_record_dne")
    def test_update_subfunction_record_dne(self) -> None:
        """Fail Case: Update a `SubFunction` that does not exist."""

        with pytest.raises(DirectoryError):
            _ = SubFunction.update_subfunction(
                subfunction_id=arguments.UPDATE_SUBFUNCTION_ID_DNE,
                name=arguments.UPDATE_SUBFUNCTION_NAME,
                description=arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                function=arguments.UPDATE_SUBFUNCTION_FUNCTION_ID,
            )

    @tag("controllers.subfunction.update_subfunction_duplicate_name")
    def test_update_subfunction_duplicate_name(self) -> None:
        """Fail Case: Update a `SubFunction` record with a duplicate name."""

        with pytest.raises(DirectoryError):
            _ = SubFunction.update_subfunction(
                subfunction_id=arguments.UPDATE_SUBFUNCTION_ID,
                name=arguments.UPDATE_SUBFUNCTION_DUPLICATE_NAME,
                description=arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                function=arguments.UPDATE_SUBFUNCTION_FUNCTION_ID,
            )

    @tag("controllers.subfunction.update_subfunction_function_dne")
    def test_update_subfunction_function_dne(self) -> None:
        """Fail Case: Update a `SubFunction` record with a given
        function id where that `Function` does not exist."""

        with pytest.raises(DirectoryError):
            _ = SubFunction.update_subfunction(
                subfunction_id=arguments.UPDATE_SUBFUNCTION_ID,
                name=arguments.UPDATE_SUBFUNCTION_NAME,
                description=arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                function=arguments.UPDATE_SUBFUNCTION_FUNCTION_ID_DNE,
            )
