"""
Collection of pytests for SubFunction's create controller.
"""

import pytest
from typing import List

from django.test import tag

from directory.controllers import SubFunction
from directory.controllers.SubFunction.tests.mutations.create.default import arguments
from directory.exceptions import DirectoryError
from directory.models.SubFunction import SubFunction as SubfunctionModel
from directory.models.SubFunction.serializers import SubFunctionSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestCreateSubFunction",
    "directory.subfunction.create",
    "subfunction.create.default",
)
class TestCreateSubFunction(MultiDBTestCase):
    """Test suite for SubFunction's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.create_subfunction")
    def test_create_subfunction(self) -> None:
        """Success Case: Create a `SubFunction` record."""

        subfunction = SubFunction.create_subfunction(
            name=arguments.CREATE_SUBFUNCTION_NAME,
            description=arguments.CREATE_SUBFUNCTION_DESCRIPTION,
            function=arguments.CREATE_SUBFUNCTION_FUNCTION_ID,
        )

        self.assertIsInstance(subfunction, SubfunctionModel)

        # Serialize `SubFunction`.
        serialized_subfunction = SubFunctionSerializer(subfunction).data

        # Remove dynamic subfunction's primary key, datetime fields,
        # function datetime fields before comparison.
        del serialized_subfunction["created"]
        del serialized_subfunction["id"]
        del serialized_subfunction["modified"]
        del serialized_subfunction["function"]["created"]
        del serialized_subfunction["function"]["modified"]

        self.assertEqual(
            serialized_subfunction, arguments.CREATE_SUBFUNCTION_EXPECTED_VALUES
        )

    @tag("controllers.subfunction.create_subfunction_duplicate_name")
    def test_create_subfunction_duplicate_name(self) -> None:
        """Fail Case: Create a `SubFunction` record with a duplicate name."""

        with pytest.raises(DirectoryError):
            _ = SubFunction.create_subfunction(
                name=arguments.CREATE_SUBFUNCTION_DUPLICATE_NAME,
                description=arguments.CREATE_SUBFUNCTION_DESCRIPTION,
                function=arguments.CREATE_SUBFUNCTION_FUNCTION_ID,
            )

    @tag("controllers.subfunction.create_subfunction_function_dne")
    def test_create_subfunction_function_dne(self) -> None:
        """Fail Case: Create a `SubFunction` record with a given
        function id where that `Function` does not exist."""

        with pytest.raises(DirectoryError):
            _ = SubFunction.create_subfunction(
                name=arguments.CREATE_SUBFUNCTION_NAME,
                description=arguments.CREATE_SUBFUNCTION_DESCRIPTION,
                function=arguments.CREATE_SUBFUNCTION_FUNCTION_DNE,
            )
