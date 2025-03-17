"""
Collection of pytests for the Resource's search controller
using `default` structure.
"""

# pylint: disable=duplicate-code,line-too-long,too-many-public-methods,wrong-import-order
import pytest
from typing import List

from django.test import tag

from directory.controllers.Resource.Resource import ResourceSearch, SearchParams
from directory.controllers.Resource.tests.query.search import arguments
from directory.controllers.Resource.tests.query.search.default import (
    arguments as search_default_arguments,
)
from directory.controllers.Resource.tests.query.search.helper import (
    TestCaseUtility,
)
from directory.exceptions import DirectoryError
from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "directory",
    "resource",
    "controllers.TestResourceSearchDefault",
    "directory.resource.search",
    "resource.search.default",
)
class TestResourceSearchDefault(TestCaseUtility):
    """Test suite for Resource's search controller using `default` structure."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/query/search/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/dispositions.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/visits.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/favorites.json",
    ]

    # **************** Test Functions *********************************

    @tag("controllers.resource.search_default_all_resources")
    def test_search_default_all_resources_in_queryset(self) -> None:
        """Success Case: Search for all `active` and `APPROVED`
        `Resource`s and get back result in `QuerySet` form."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.VALID_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_downloadable_resources")
    def test_search_default_for_downloadable_resources(self) -> None:
        """Success Case: Search for `Resource`s that have their field: `download`
        equal to True."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "download": True,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_DOWNLOADABLE_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_nondownloadable_resources")
    def test_search_default_for_non_downloadable_resources(self) -> None:
        """Success Case: Search for `Resource`s that have their field: `download`
        equal to False."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "download": False,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_NON_DOWNLOADABLE_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_name")
    def test_search_default_by_resource_name(self) -> None:
        """Success Case: Search for a matching `Resource` by name."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "name": search_default_arguments.SEARCH_BY_NAME,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_NAME_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_description")
    def test_search_default_by_resource_description(self) -> None:
        """Success Case: Search for a matching `Resource` by description."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "description": search_default_arguments.SEARCH_BY_DESCRIPTION,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_DESCRIPTION_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_functions_subfunctions")
    def test_search_default_by_resource_functions_subfunctions(self) -> None:
        """Success Case: Search for `Resource`s by functions and subfunctions."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_FUNCTION_IDS,
            "subfunctions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_SUBFUNCTION_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_functions_employee_levels")
    def test_search_default_by_resource_functions_employee_levels(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions and employee
        levels."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_functions_tags")
    def test_search_default_by_resource_functions_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions and tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_TAGS_FUNCTION_IDS,
            "tags": search_default_arguments.SEARCH_BY_FUNCTION_TAGS_TAG_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_TAGS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_subfunctions_employee_levels")
    def test_search_default_by_resource_subfunctions_employee_levels(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by subfunctions and
        employee levels."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_subfunctions_tags")
    def test_search_default_by_resource_subfunctions_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by subfunctions and
        tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_TAGS_SUBFUNCTION_IDS,
            "tags": search_default_arguments.SEARCH_BY_SUBFUNCTION_TAGS_TAG_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_TAGS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_employee_levels_tags")
    def test_search_default_by_resource_employee_levels_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by employee levels and
        tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "employee_levels": search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS,
            "tags": search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_TAGS_TAG_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS,
        )

    @tag(
        "controllers.resource.search_default_resource_functions_subfunctions_employee_levels"
    )
    def test_search_default_by_resource_functions_subfunctions_employee_levels(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions, subfunctions and
        employee levels."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS,
            "subfunctions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS,
        )

    @tag(
        "controllers.resource.search_default_resource_functions_subfunctions_employee_levels_tags"
    )
    def test_search_default_by_resource_functions_subfunctions_employee_levels_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions, subfunctions,
        employee levels and tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_FUNCTION_IDS,
            "subfunctions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS,
            "tags": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS,
        )

    @tag(
        "controllers.resource.search_default_resource_subfunctions_employee_levels_tags"
    )
    def test_search_default_by_resource_subfunctions_employee_levels_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by subfunctions, employee
        levels and tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS,
            "tags": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_functions")
    def test_search_default_by_resource_functions(self) -> None:
        """Success Case: Search for `Resource`s by functions."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_subfunctions")
    def test_search_default_by_resource_subfunctions(self) -> None:
        """Success Case: Search for `Resource`s by subfunctions."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_employee_levels")
    def test_search_default_by_resource_employee_levels(self) -> None:
        """Success Case: Search for `Resource`s by employee levels."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "employee_levels": search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_tags")
    def test_search_default_by_resource_tags(self) -> None:
        """Success Case: Search for `Resource`s by tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "tags": search_default_arguments.SEARCH_BY_TAGS_IDS,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_TAGS_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_resource_name_dne")
    def test_search_default_by_resource_name_dne(self) -> None:
        """Success Case: Search for `Resource`s by name, but receive an
        empty QuerySet due to no existing `Resource` having a matching
        name."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "name": arguments.SEARCH_BY_NAME_DNE,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_resource_description_dne")
    def test_search_default_by_resource_description_dne(self) -> None:
        """Success Case: Search for `Resource`s by description, but
        receive an empty QuerySet due to no existing `Resource` having
        a matching description."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "description": arguments.SEARCH_BY_DESCRIPTION_DNE,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_resource_functions_dne")
    def test_search_default_by_resource_functions_dne(self) -> None:
        """Success Case: Search for `Resource`s by functions, but
        receive an empty QuerySet due to no existing `Resource` having
        matching functions."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": arguments.SEARCH_BY_FUNCTIONS_DNE,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_resource_subfunctions_dne")
    def test_search_default_by_resource_subfunctions_dne(self) -> None:
        """Success Case: Search for `Resource`s by subfunctions, but
        receive an empty QuerySet due to no existing `Resource` having
        matching subfunctions."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": arguments.SEARCH_BY_SUBFUNCTIONS_DNE,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_resource_employee_levels_dne")
    def test_search_default_by_resource_employee_levels_dne(self) -> None:
        """Success Case: Search for `Resource`s by employee levels, but
        receive an empty QuerySet due to no existing `Resource` having
        matching employee levels."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "employee_levels": arguments.SEARCH_BY_EMPLOYEE_LEVELS_DNE,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_resource_tags_dne")
    def test_search_default_by_resource_tags_dne(self) -> None:
        """Success Case: Search for `Resource`s by tags, but receive
        an empty QuerySet due to no existing `Resource` having matching
        tags."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "tags": arguments.SEARCH_BY_TAGS_DNE,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_limit_resources")
    def test_search_default_limit_resources(self) -> None:
        """Success Case: Search for `Resource`s and limit the number
        of entries being returned."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "limit": search_default_arguments.SEARCH_LIMIT_NUMBER,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_LIMIT_RESOURCE_IDS,
        )

    @tag("controllers.resource.search_default_exceeding_page_count")
    def test_search_default_empty_queryset_due_to_exceeding_page_count(self) -> None:
        """Success Case: Search for `Resource`s but using a page number
        in the search params that exceeds the number of pages after
        pagination."""

        params: SearchParams = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "page": arguments.SEARCH_EXCEEDING_PAGE_NUMBER,
        }
        resources = ResourceSearch.search(params=params)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
        )

    @tag("controllers.resource.search_default_empty_parameters")
    def test_search_default_empty_params(self) -> None:
        """Fail Case: Attempt to make a search with no parameters."""

        with pytest.raises(DirectoryError):
            _ = ResourceSearch.search(params={})  # type: ignore

    @tag("controllers.resource.search_default_incorrect_parameter_value_type")
    def test_search_default_incorrect_parameter_value_type(self) -> None:
        """Fail Case: Attempt to make a search with incorrect parameter
        value."""

        with pytest.raises(DirectoryError):
            params: SearchParams = {
                **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
                "subfunctions": [{}],  # type: ignore
            }
            _ = ResourceSearch.search(params=params)
