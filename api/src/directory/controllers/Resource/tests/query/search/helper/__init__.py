"""
Contains a helper utility class for Resource's search controller
pytests.
"""

import pytest
from cryptography.fernet import Fernet
from typing import Any, cast, List, Union

from django.db.models import QuerySet

from directory.models import Resource
from directory.models.Resource.serializers import ResourceSerializer

from manager.settings import DATA_ENCRYPTION_KEY

from manager.utils.tests import MultiDBTestCase

# Initialize cryptography module.
# Restore padding (Fernet keys are 44 chars; add '=' if needed)
FERNET_KEY = DATA_ENCRYPTION_KEY + ("=" * ((4 - len(DATA_ENCRYPTION_KEY) % 4) % 4))

fernet = Fernet(FERNET_KEY)
# Encrypted props on a `Resource` record when serialized.
ENCRYPTED_PROPS_TO_TEST = {"name", "description", "url"}


class TestCaseUtility(MultiDBTestCase):
    """
    Helper class used for Resource's search controller
    pytests.
    """

    # Properties that are only part of a search
    # where the structure is `functree` and serialize
    # is True.
    SEARCH_FUNCTREE_SERIALIZE_ONLY_PROPS: List[str] = [
        "favorited_by",
        "site",
        "restricted",
    ]

    def _resource_properties_test(
        self,
        serialized_resource: dict,
        properties_to_verify: dict,
        serialized_search: bool = False,
    ) -> None:
        """
        Tests the properties of a Resource.

        Accepts:
            * serialized_resource (dict]): A serialized version of the `Resource` in
                the form of a dict.
            * properties_to_verify (dict): Properties of the `Resource`
                that will be verified.
            * serialized_search (bool): Indicates if the search is serialized.
        Returns:
            * None
        """

        properties_to_test: dict = {**properties_to_verify}
        # If not a serialized search then remove only `functree`
        # properties from properties_to_test.
        if not serialized_search:
            for prop_to_delete in self.SEARCH_FUNCTREE_SERIALIZE_ONLY_PROPS:
                if prop_to_delete in properties_to_test:
                    properties_to_test.pop(prop_to_delete)

        for prop, value in properties_to_test.items():
            self.assertIn(prop, serialized_resource)
            # If the instance of `value` is not a list
            # then we'll perform an assertEqual(...), else
            # we'll use the list specific assertion:
            # assertCountEqual(...).
            if not isinstance(value, list):
                serialized_resource_value = serialized_resource[prop]
                # Decrypt any encrypted values on a restricted `Resource` record.
                if (
                    "restricted" in serialized_resource
                    and serialized_resource["restricted"]
                    and prop in ENCRYPTED_PROPS_TO_TEST
                ):
                    try:
                        serialized_resource_value = fernet.decrypt(
                            cast(str, serialized_resource_value).encode()
                        ).decode()
                    except (TypeError, ValueError):
                        pytest.fail("Values not encrypted.")
                self.assertEqual(serialized_resource_value, value)
            else:
                self.assertCountEqual(serialized_resource[prop], value)

    def _verify_collection_of_resources(
        self,
        resources: Union[QuerySet[Resource, Resource], dict, List[dict]],
        resource_map: dict,
        resource_ids: List[int],
        serialized_search: bool = False,
    ) -> None:
        """
        Verifies the collection of `Resource`s given.

        Accepts:
            * resources (Union[QuerySet[Resource], dict, List[dict]):
                Collection of `Resources` to verify.
            * resource_map (dict): Dictionary containing collection
                of serialized `Resource`s to test against.
            * resource_ids (List[int]): The ids of the resources
                to be used for validating the resources against the
                entries in the `VALID_RESOURCE_MAP`.
            * serialized_search (bool): Indicates if a serialized
                search is being verified.
        Returns:
            * None
        """

        self.assertEqual(len(resources), len(resource_ids))
        resource_collection_class_type = (
            QuerySet[Resource, Resource] if not serialized_search else List
        )
        self.assertIsInstance(resources, resource_collection_class_type)
        resource_class_type = Resource if not serialized_search else dict
        for resource in resources:
            self.assertIsInstance(resource, resource_class_type)
            serialized_resource: dict = (
                ResourceSerializer(resource).data if not serialized_search else resource
            )
            resource_id: int = serialized_resource["id"]
            self.assertIn(resource_id, resource_ids)
            self._resource_properties_test(
                serialized_resource=serialized_resource,
                properties_to_verify=resource_map[resource_id],
                serialized_search=serialized_search,
            )

    def _verify_functree_structure_search_results(
        self,
        search_results: Union[dict, Any],
        resource_map: dict,
        validation_map: dict,
        serialized: bool = False,
    ) -> None:
        """
        Verifies the search results on a search made with
        `functree` structure.

        Accepts:
            * search_results (dict): The return dictionary from
                a search done where the `functree` structure was
                used.
            * resources_map (dict): A dictionary containing all
                valid resources.
            * validation_map (dict): The dictionary to be used to
                validate the `functree` search results.
            * serialized (bool): Indicates whether the collection
                of `Resource`s in the search is serialized.
        Returns:
            * None
        """

        # Assert the function names match.
        self.assertCountEqual(
            list(search_results.keys()),
            list(validation_map.keys()),
        )
        for (
            function_name,
            subfunction_collection,
        ) in validation_map.items():
            # Assert the subfunction names match.
            self.assertCountEqual(
                list(search_results[function_name].keys()),
                list(subfunction_collection.keys()),
            )
            for subfunction_name, resource_ids in subfunction_collection.items():
                search_results_resources_for_subfunction: Union[
                    QuerySet[Resource, Resource], List[dict]
                ] = search_results[function_name][subfunction_name]
                self._verify_collection_of_resources(
                    resources=search_results_resources_for_subfunction,
                    resource_map=resource_map,
                    resource_ids=resource_ids,
                    serialized_search=serialized,
                )
