"""
Collection of pytests for the Resource's search view
endpoint using `default` structure.
"""

# pylint: disable=duplicate-code,line-too-long,too-many-public-methods
from typing import List

from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.Resource.tests.query.search import arguments
from directory.controllers.Resource.tests.query.search.default import (
    arguments as search_default_arguments,
)
from directory.controllers.Resource.tests.query.search.helper import (
    TestCaseUtility,
)
from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "directory",
    "resource",
    "views",
    "directory.resource.search",
    "resource.search.default",
    "views.TestResourceSearchDefault",
)
class TestResourceSearchDefault(TestCaseUtility):
    """
    Test for POST /v1/directory/resource/search endpoint
    using `default` structure.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/query/search/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/dispositions.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/visits.json",
        "directory/controllers/Resource/tests/query/search/default/fixtures/favorites.json",
    ]

    url = reverse("directory.resource.search")

    # **************** Test Functions *********************************

    @tag("views.resource.search_default_all_resources")
    def test_search_default_all_resources_in_queryset(self) -> None:
        """Success Case: Search for all `active` and `APPROVED`
        `Resource`s and get back result in `QuerySet` form."""

        body: dict = {**search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS}
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.VALID_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_downloadable_resources")
    def test_search_default_for_downloadable_resources(self) -> None:
        """Success Case: Search for `Resource`s that have their field: `download`
        equal to True."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "download": True,
        }

        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_DOWNLOADABLE_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_nondownloadable_resources")
    def test_search_default_for_non_downloadable_resources(self) -> None:
        """Success Case: Search for `Resource`s that have their field: `download`
        equal to False."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "download": False,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_NON_DOWNLOADABLE_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_name")
    def test_search_default_by_resource_name(self) -> None:
        """Success Case: Search for a matching `Resource` by name."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "name": search_default_arguments.SEARCH_BY_NAME,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_NAME_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_description")
    def test_search_default_by_resource_description(self) -> None:
        """Success Case: Search for a matching `Resource` by description."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "description": search_default_arguments.SEARCH_BY_DESCRIPTION,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_DESCRIPTION_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_functions_subfunctions")
    def test_search_default_by_resource_functions_subfunctions(self) -> None:
        """Success Case: Search for `Resource`s by functions and subfunctions."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_FUNCTION_IDS,
            "subfunctions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_SUBFUNCTION_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_functions_employee_levels")
    def test_search_default_by_resource_functions_employee_levels(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions and employee
        levels."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_functions_tags")
    def test_search_default_by_resource_functions_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions and tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_TAGS_FUNCTION_IDS,
            "tags": search_default_arguments.SEARCH_BY_FUNCTION_TAGS_TAG_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_TAGS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_subfunctions_employee_levels")
    def test_search_default_by_resource_subfunctions_employee_levels(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by subfunctions and
        employee levels."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_subfunctions_tags")
    def test_search_default_by_resource_subfunctions_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by subfunctions and
        tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_TAGS_SUBFUNCTION_IDS,
            "tags": search_default_arguments.SEARCH_BY_SUBFUNCTION_TAGS_TAG_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_TAGS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_employee_levels_tags")
    def test_search_default_by_resource_employee_levels_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by employee levels and
        tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "employee_levels": search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS,
            "tags": search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_TAGS_TAG_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag(
        "views.resource.search_default_resource_functions_subfunctions_employee_levels"
    )
    def test_search_default_by_resource_functions_subfunctions_employee_levels(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions, subfunctions and
        employee levels."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS,
            "subfunctions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag(
        "views.resource.search_default_resource_functions_subfunctions_employee_levels_tags"
    )
    def test_search_default_by_resource_functions_subfunctions_employee_levels_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by functions, subfunctions,
        employee levels and tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_FUNCTION_IDS,
            "subfunctions": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS,
            "tags": search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_subfunctions_employee_levels_tags")
    def test_search_default_by_resource_subfunctions_employee_levels_tags(
        self,
    ) -> None:
        """Success Case: Search for `Resource`s by subfunctions, employee
        levels and tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS,
            "employee_levels": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS,
            "tags": search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_functions")
    def test_search_default_by_resource_functions(self) -> None:
        """Success Case: Search for `Resource`s by functions."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": search_default_arguments.SEARCH_BY_FUNCTION_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_FUNCTION_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_subfunctions")
    def test_search_default_by_resource_subfunctions(self) -> None:
        """Success Case: Search for `Resource`s by subfunctions."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": search_default_arguments.SEARCH_BY_SUBFUNCTION_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_SUBFUNCTION_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_employee_levels")
    def test_search_default_by_resource_employee_levels(self) -> None:
        """Success Case: Search for `Resource`s by employee levels."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "employee_levels": search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_EMPLOYEE_LEVELS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_tags")
    def test_search_default_by_resource_tags(self) -> None:
        """Success Case: Search for `Resource`s by tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "tags": search_default_arguments.SEARCH_BY_TAGS_IDS,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_BY_TAGS_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_name_dne")
    def test_search_default_by_resource_name_dne(self) -> None:
        """Success Case: Search for `Resource`s by name, but receive an
        empty QuerySet due to no existing `Resource` having a matching
        name."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "name": arguments.SEARCH_BY_NAME_DNE,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_description_dne")
    def test_search_default_by_resource_description_dne(self) -> None:
        """Success Case: Search for `Resource`s by description, but
        receive an empty QuerySet due to no existing `Resource` having
        a matching description."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "description": arguments.SEARCH_BY_DESCRIPTION_DNE,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_functions_dne")
    def test_search_default_by_resource_functions_dne(self) -> None:
        """Success Case: Search for `Resource`s by functions, but
        receive an empty QuerySet due to no existing `Resource` having
        matching functions."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "functions": arguments.SEARCH_BY_FUNCTIONS_DNE,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_subfunctions_dne")
    def test_search_default_by_resource_subfunctions_dne(self) -> None:
        """Success Case: Search for `Resource`s by subfunctions, but
        receive an empty QuerySet due to no existing `Resource` having
        matching subfunctions."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": arguments.SEARCH_BY_SUBFUNCTIONS_DNE,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_employee_levels_dne")
    def test_search_default_by_resource_employee_levels_dne(self) -> None:
        """Success Case: Search for `Resource`s by employee levels, but
        receive an empty QuerySet due to no existing `Resource` having
        matching employee levels."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "employee_levels": arguments.SEARCH_BY_EMPLOYEE_LEVELS_DNE,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_resource_tags_dne")
    def test_search_default_by_resource_tags_dne(self) -> None:
        """Success Case: Search for `Resource`s by tags, but receive
        an empty QuerySet due to no existing `Resource` having matching
        tags."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "tags": arguments.SEARCH_BY_TAGS_DNE,
        }
        response = self.client.post(self.url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_limit_resources")
    def test_search_default_limit_resources(self) -> None:
        """Success Case: Search for `Resource`s and limit the number
        of entries being returned."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
        }
        request_url: str = (
            f"{self.url}?limit={search_default_arguments.SEARCH_LIMIT_NUMBER}"
        )
        response = self.client.post(request_url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=search_default_arguments.SEARCH_LIMIT_RESOURCE_IDS,
            serialized_search=True,
        )

    @tag("views.resource.search_default_exceeding_page_count")
    def test_search_default_empty_queryset_due_to_exceeding_page_count(self) -> None:
        """Success Case: Search for `Resource`s but using a page number
        in the search params that exceeds the number of pages after
        pagination."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
        }
        request_url: str = f"{self.url}?page={arguments.SEARCH_EXCEEDING_PAGE_NUMBER}"
        response = self.client.post(request_url, body, content_type="application/json")
        resources = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._verify_collection_of_resources(
            resources=resources,
            resource_map=search_default_arguments.VALID_RESOURCE_MAP,
            resource_ids=[],
            serialized_search=True,
        )

    @tag("views.resource.search_default_incorrect_parameter_value_type")
    def test_search_default_incorrect_parameter_value_type(self) -> None:
        """Fail Case: Attempt to make a search with incorrect parameter
        value."""

        body: dict = {
            **search_default_arguments.BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS,
            "subfunctions": [{}],
        }
        response = self.client.post(self.url, body, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
