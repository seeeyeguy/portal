"""
Collection of pytests for Function's update controller.
"""
import pytest
from typing import List

from django.test import tag, TestCase

from directory.controllers import Function
from directory.controllers.Function.tests.mutations.update.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Function import Function as FunctionModel
from directory.models.Function.serializers import FunctionSerializer


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestUpdateFunction",
    "directory.function.update",
    "function.update.default",
)
class TestUpdateFunction(TestCase):
    """Test suite for Function's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.update_function")
    def test_update_function(self) -> None:
        """Success Case: Update a `Function` record."""

        # Update `Function` record.
        function_record, _ = Function.update_function(
            function_id=arguments.UPDATE_FUNCTION_ID,
            name=arguments.UPDATE_FUNCTION_NAME,
            description=arguments.UPDATE_FUNCTION_DESCRIPTION,
        )

        self.assertIsInstance(function_record, FunctionModel)

        # Serialize `Function`.
        serialized_function = FunctionSerializer(function_record).data

        self.assertEqual(serialized_function, arguments.UPDATE_FUNCTION_EXPECTED_VALUES)

    @tag("controllers.function.update_function_record_dne")
    def test_update_function_record_dne(self) -> None:
        """Fail Case: Update a `Function` that does not exist."""

        with pytest.raises(DirectoryError):
            _ = Function.update_function(
                function_id=arguments.UPDATE_FUNCTION_ID_DNE,
                name=arguments.UPDATE_FUNCTION_NAME,
                description=arguments.UPDATE_FUNCTION_DESCRIPTION,
            )

    @tag("controllers.function.update_function_duplicate_name")
    def test_update_function_duplicate_name(self) -> None:
        """Fail Case: Update a `Function` record with a duplicate name."""

        with pytest.raises(DirectoryError):
            _ = Function.update_function(
                function_id=arguments.UPDATE_FUNCTION_ID_DUPLICATE,
                name=arguments.UPDATE_FUNCTION_DUPLICATE_NAME,
                description=arguments.UPDATE_FUNCTION_DESCRIPTION,
            )
