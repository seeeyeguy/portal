"""
Collection of pytests for SubFunction's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from directory.controllers.SubFunction.SubFunction import SubFunction
from directory.controllers.SubFunction.tests.query.read.default import arguments
from directory.exceptions import DirectoryError
from directory.models.SubFunction.SubFunction import (
    SubFunction as SubFunctionModel,
)
from directory.models.SubFunction.serializers import SubFunctionSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestFetchSubFunction",
    "directory.subfunction.fetch",
    "subfunction.fetch.default",
)
class TestFetchSubFunction(MultiDBTestCase):
    """Test suite for SubFunction's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.fetch_subfunctions")
    def test_fetch_subfunctions(self) -> None:
        """Success Case: Fetch all `SubFunction` records."""

        subfunctions = SubFunction.fetch_subfunctions()

        self.assertIsInstance(subfunctions, QuerySet[SubFunctionModel])
        self.assertEqual(
            subfunctions.count(), len(arguments.VALID_SUBFUNCTION_RECORDS.keys())  # type: ignore[union-attr]
        )

        for subfunction in subfunctions:  # type: ignore[union-attr]
            self.assertIsInstance(subfunction, SubFunctionModel)

            subfunction_id: int = subfunction.id

            self.assertIn(subfunction_id, arguments.VALID_SUBFUNCTION_RECORDS)
            self.assertEqual(
                SubFunctionSerializer(subfunction).data,
                arguments.VALID_SUBFUNCTION_RECORDS[subfunction_id],
            )

    @tag("controllers.subfunction.fetch_subfunction_by_id")
    def test_fetch_subfunction_by_id(self) -> None:
        """Success Case: Fetch a `SubFunction` record given an id."""

        subfunction = SubFunction.fetch_subfunctions(
            subfunction_id=arguments.FETCH_SUBFUNCTION_BY_ID
        )

        self.assertIsInstance(subfunction, SubFunctionModel)

        subfunction_id: int = subfunction.id  # type: ignore[union-attr]

        self.assertIn(subfunction_id, arguments.VALID_SUBFUNCTION_RECORDS)
        self.assertEqual(
            SubFunctionSerializer(subfunction).data,
            arguments.VALID_SUBFUNCTION_RECORDS[subfunction_id],
        )

    @tag("controllers.subfunction.fetch_subfunction_by_id_dne")
    def test_fetch_subfunction_by_id_dne(self) -> None:
        """Fail Case: Fetch a `SubFunction` record given an id where
        record does not exist."""

        with pytest.raises(DirectoryError):
            _ = SubFunction.fetch_subfunctions(
                subfunction_id=arguments.FETCH_SUBFUNCTION_BY_ID_DNE
            )
