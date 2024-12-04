"""
Collection of pytests for Function's fetch controller.
"""

import pytest
from typing import List, Union

from django.db.models import QuerySet
from django.test import tag, TestCase

from directory.controllers.Function.Function import Function
from directory.controllers.Function.tests.query.read.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Function.Function import (
    Function as FunctionModel,
)
from directory.models.Function.serializers import FunctionSerializer


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestFetchFunction",
    "directory.function.fetch",
    "function.fetch.default",
)
class TestFetchFunction(TestCase):
    """Test suite for Function's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.fetch_functions")
    def test_fetch_functions(self) -> None:
        """Success Case: Fetch all `Function` records."""

        functions = Function.fetch_functions()

        self.assertIsInstance(functions, QuerySet[FunctionModel])
        self.assertEqual(
            functions.count(), len(arguments.VALID_FUNCTION_RECORDS.keys())  # type: ignore[union-attr]
        )

        for function in functions:  # type: ignore[union-attr]
            self.assertIsInstance(function, FunctionModel)
            function_id: int = function.id
            self.assertIn(function_id, arguments.VALID_FUNCTION_RECORDS)
            self.assertEqual(
                FunctionSerializer(function).data,
                arguments.VALID_FUNCTION_RECORDS[function_id],
            )

    @tag("controllers.function.fetch_function_by_id")
    def test_fetch_function_by_id(self) -> None:
        """Success Case: Fetch a `Function` record given an id."""

        function: Union[
            FunctionModel, QuerySet[FunctionModel, FunctionModel]
        ] = Function.fetch_functions(function_id=arguments.FETCH_FUNCTION_BY_ID)

        self.assertIsInstance(function, FunctionModel)
        function_id: int = function.id  # type: ignore[union-attr]
        self.assertIn(function_id, arguments.VALID_FUNCTION_RECORDS)
        self.assertEqual(
            FunctionSerializer(function).data,
            arguments.VALID_FUNCTION_RECORDS[function_id],
        )

    @tag("controllers.function.fetch_function_by_id_dne")
    def test_fetch_function_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Function` record given an id where
        record does not exist."""

        with pytest.raises(DirectoryError):
            _ = Function.fetch_functions(function_id=arguments.FETCH_FUNCTION_BY_ID_DNE)
