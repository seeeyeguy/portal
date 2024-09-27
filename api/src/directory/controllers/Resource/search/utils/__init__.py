"""
`Resource` search utils module. These utils provide
helper functions to search and format results from
the database.
"""

from typing import cast, List, TypedDict, Union

from django.db.models import QuerySet

from directory.models import Function, Resource, SubFunction, Tag
from directory.models.Resource.serializers import ResourceSerializer


FUNCTREE_STRUCTURE = "functree"
DEFAULT_STRUCTURE = "default"


def structure_resources(resources: QuerySet[Resource], serialize: bool = False) -> dict:
    """
    Returns a dictionary with a custom structure for grouping
    `Resource`s by subfunctions and their parent functions.

    Accepts:
        * resources (QuerySet[Resource]): Collection of
            `Resource`s that will be part of the custom
            structure.
        * serialize (bool): Flag indicating if the collection
            of `Resource`s inside the structure will be
            QuerySet[Resource](False) or a List[dict](True).
    Returns:
        * structure (dict): A dictionary containing a collection
                of `Resource`s grouped by subfunctions and their
                parent functions.
    """

    def construct_serialized_resource_data(resource: Resource) -> dict:
        """
        Constructs a dictonary containing the serialized data, including
        additional meta fields, for the given `Resource`.

        Accepts:
            * resource (Resource): `Resource` instance that will
                have its data serialized.
        Returns:
            * serialized_resource_data (dict): A dictionary containing
                the serialized resource's data, including additional
                meta fields.
                - Meta Fields:
                    -- favorited_by: List of users who favorited the
                        `Resource`.
                    -- restricted: List of access permissions.
                    -- site: List of locations related to the `Resource`.
        """

        # Create dictionary from the serialized `resource` data.
        serialized_resource_data: dict = {**ResourceSerializer(resource).data}

        # Construct list of emails of the `User`s that favorited this
        # `Resource` and assign it to the `favorited_by` key.
        resource_favorited_by: List[str] = list(
            resource.favorites.values_list("user__email", flat=True)
        )
        serialized_resource_data["favorited_by"] = resource_favorited_by

        # Get associated `Tag`s for this `Resource`.
        resource_tags: QuerySet[Tag] = resource.tags.all()

        # Filter `resource_tags` for entries where the `label` starts with
        # `filter::site:` prefix.
        tag_filter_site_labels: List[str] = list(
            resource_tags.filter(label__startswith="filter::site:").values_list(
                "label", flat=True
            )
        )
        # Replace `filter::site:` prefix from labels in `tag_filter_site_labels`.
        tag_filter_site_labels = [
            label.replace("filter::site:", "") for label in tag_filter_site_labels
        ]
        # Assign `tag_filter_site_labels` to `site` key.
        serialized_resource_data["site"] = tag_filter_site_labels

        # Filter `resource_tags` for entries where the `label` starts with
        # `restricted::` prefix.
        tag_restricted_labels: List[str] = list(
            resource_tags.filter(label__startswith="restricted::").values_list(
                "label", flat=True
            )
        )
        # Replace `restricted::` prefix from labels in `tag_restricted_labels`.
        tag_restricted_labels = [
            label.replace("restricted::", "") for label in tag_restricted_labels
        ]

        # Dictionary containing the key-value pairs derived from
        # the restricted labels.
        restricted_dict: dict = {}
        # Loop through the restricted labels.
        for restricted_label in tag_restricted_labels:
            # Extract the restricted key and value from the label.
            restricted_key, restricted_value = restricted_label.split(":")
            # If the restricted key is not in restricted_dict then add
            # it and initialize its value to an empty list.
            if restricted_key not in restricted_dict:
                restricted_dict[restricted_key] = []
            # Append the restricted value to the corresponding list
            # assigned to restricted key.
            restricted_dict[restricted_key].append(restricted_value)

        # Assign `tag_restricted_labels` to `restricted` key.
        serialized_resource_data["restricted"] = restricted_dict
        return serialized_resource_data

    # Initialize `structure` with an empty dictionary.
    structure: dict = {}
    # Loop through collection of given `Resource`s.
    for resource in resources:
        # Get the QuerySet of `SubFunction`s for the `Resource`
        # and loop through them.
        subfunctions: QuerySet[SubFunction] = cast(
            QuerySet[SubFunction], resource.subfunctions.all()
        )

        for subfunction in cast(List[SubFunction], subfunctions):
            # Get the name of the `SubFunction`'s
            # linked `Function`.
            function_name: str = cast(Function, subfunction.function).name

            # If `function_name` is not an existing key
            # inside `structure` then add an empty dict
            # value to this key.
            if function_name not in structure:
                structure[function_name] = {}

            # Get the name of the `SubFunction`.
            subfunction_name: str = subfunction.name
            # If the subfunction_name is not an existing
            # key inside the `structure[function_name]` dict,
            # then add it as a key and assign either an
            # empty `Resource` QuerySet if `serialize==False`
            # or an empty list otherwise.
            if subfunction_name not in structure[function_name]:
                structure[function_name][subfunction_name] = (
                    [] if serialize else Resource.objects.none()
                )
            # If `serialize` is true then add a serialized version
            # of the `Resource`, else append the `Resource` instance to
            # the QuerySet[Resource] under the subfunction.
            if serialize:
                data: dict = construct_serialized_resource_data(resource)
                structure[function_name][subfunction_name].append(data)
            else:
                structure[function_name][subfunction_name] = structure[function_name][
                    subfunction_name
                ] | Resource.objects.filter(id=resource.id)

    return structure
