"""
`Resource` search utils module. These utils provide
helper functions to search and format results from
the database.
"""

from cryptography.fernet import Fernet
from typing import cast, List

from django.db.models import QuerySet

from directory.models import Function, Resource, SubFunction, Tag
from directory.models.Resource.serializers import ResourceSerializer

from manager.settings import DATA_ENCRYPTION_KEY

FUNCTREE_STRUCTURE: str = "functree"
DEFAULT_STRUCTURE: str = "default"

GENERAL_SUBFUNCTION_NAME: str = "General"

# Initialize cryptography module.
# Restore padding (Fernet keys are 44 chars; add '=' if needed)
FERNET_KEY = DATA_ENCRYPTION_KEY + ("=" * ((4 - len(DATA_ENCRYPTION_KEY) % 4) % 4))

fernet = Fernet(FERNET_KEY)


def structure_resources(
    resources: QuerySet[Resource, Resource], serialize: bool = False
) -> dict:
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
        Constructs a dictionary containing the serialized data, including
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
        resource_tags: QuerySet[Tag, Tag] = resource.tags.all()

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
        # If the `Resource` record has restricted tags, encrypt sensitive data
        # with the encryption key.
        if restricted_dict:
            # Encrypt data.
            encrypted_resource_name = fernet.encrypt(
                cast(str, serialized_resource_data["name"]).encode()
            )
            encrypted_resource_description = fernet.encrypt(
                cast(str, serialized_resource_data["description"]).encode()
            )
            encrypted_resource_url = fernet.encrypt(
                cast(str, serialized_resource_data["url"]).encode()
            )
            # Assign encrypted data.
            serialized_resource_data["name"] = encrypted_resource_name.decode()
            serialized_resource_data[
                "description"
            ] = encrypted_resource_description.decode()
            serialized_resource_data["url"] = encrypted_resource_url.decode()

        return serialized_resource_data

    # Initialize `structure` with an empty dictionary.
    structure: dict = {}
    # Loop through collection of given `Resource`s.
    for resource in resources:
        # Get the QuerySet of `SubFunction`s for the `Resource`
        # and loop through them.
        subfunctions: QuerySet[SubFunction, SubFunction] = cast(
            QuerySet[SubFunction, SubFunction], resource.subfunctions.all()
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
            subfunction_name: str = (
                GENERAL_SUBFUNCTION_NAME
                if f"{GENERAL_SUBFUNCTION_NAME}::" in subfunction.name
                else subfunction.name
            )
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

    # Loop through the `structure` in order to re-order
    # the collection assigned to each `Function` name to
    # follow the alphabetical order of the `SubFunction`
    # name, with the special case that if the `SubFunction`
    # name is equal to `GENERAL_SUBFUNCTION_NAME` that will
    # be placed first.
    for function_name, subfunction_collection in structure.items():
        # Generate sorted list of `SubFunction` names from
        # the keys of the `subfunction_collection`.
        subfunction_names: List[str] = list(
            sorted(subfunction_collection.keys(), key=str.lower)
        )
        # If `GENERAL_SUBFUNCTION_NAME` is in `subfunction_names`,
        # then proceed to move it to the beginning of the list.
        if GENERAL_SUBFUNCTION_NAME in subfunction_names:
            subfunction_names.insert(
                0,
                subfunction_names.pop(
                    subfunction_names.index(GENERAL_SUBFUNCTION_NAME)
                ),
            )
        # Assign a new collection to the structure for the current
        # `function_name` that follows the order in `subfunction_names`.
        structure[function_name] = {
            subfunction_name: structure[function_name][subfunction_name]
            for subfunction_name in subfunction_names
        }

    return structure
