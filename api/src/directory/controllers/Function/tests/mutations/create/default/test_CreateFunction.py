"""
Collection of pytests for Function's create controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import List

from django.test import tag

from directory.controllers import Function
from directory.controllers.Function.tests.mutations.create.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Function import Function as FunctionModel
from directory.models.Function.serializers import FunctionSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestCreateFunction",
    "directory.function.create",
    "function.create.default",
)
class TestCreateFunction(MultiDBTestCase):
    """Test suite for Function's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.create_function")
    def test_create_function(self) -> None:
        """Success Case: Create a `Function` record."""

        function = Function.create_function(
            name=arguments.CREATE_FUNCTION_NAME,
            description=arguments.CREATE_FUNCTION_DESCRIPTION,
        )

        self.assertIsInstance(function, FunctionModel)

        # Serialize `Function`.
        serialized_function = FunctionSerializer(function).data

        # Remove dynamic primary key and datetime fields before comparison.
        del serialized_function["created"]
        del serialized_function["id"]
        del serialized_function["modified"]

        self.assertEqual(serialized_function, arguments.CREATE_FUNCTION_EXPECTED_VALUES)

    @tag("controllers.function.create_function_duplicate_name")
    def test_create_function_duplicate_name(self) -> None:
        """Fail Case: Create a `Function` record with a duplicate name."""

        with pytest.raises(DirectoryError):
            _ = Function.create_function(
                name=arguments.CREATE_FUNCTION_DUPLICATE_NAME,
                description=arguments.CREATE_FUNCTION_DESCRIPTION,
            )
