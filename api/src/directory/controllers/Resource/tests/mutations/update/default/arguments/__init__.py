"""
Arguments to be shared for Resource's update
controller pytests.
"""

from typing import List

from directory.controllers.Resource.Resource import UpdateResourceParams

# User email used when testing `Resource` update view.
UPDATE_RESOURCE_USER_EMAIL: str = "May.Parker@harris.com"

# User email used when testing `Resource` update with a
# `User` that does not have `Access` with a valid `Role`.
UPDATE_RESOURCE_USER_EMAIL_INVALID_ROLE: str = "Ben.Parker@harris.com"

# `User` email used when testing `Resource` update with a
# `User` that does not have `Access` to update a `Resource`
# within a set of given `SubFunction`s.
UPDATE_RESOURCE_USER_EMAIL_SUBFUNCTIONS_PERMISSIONS_DENIED: str = (
    "Miles.Morales@harris.com"
)

# Id of `Resource` for testing successful `Resource` update.
UPDATE_RESOURCE_ID: int = 2

# Base parameters used for successful `Resource` update.
BASE_UPDATE_RESOURCE_STRUCTURE_PARAMS: UpdateResourceParams = {
    "resource_id": UPDATE_RESOURCE_ID,
    "name": "Test Update Name.",
    "url": "https://www.test-site.com",
    "thumbnail": None,  # type: ignore[typeddict-item,unused-ignore]
    "description": "Test resource description for update tests.",
    "employee_levels": [2],
    "subfunctions": [1],
    "tags": [1, 5],
    "type": "test update type",
    "download": False,
}

# Expected number of affected rows after successful `Resource` update.
UPDATE_RESOURCE_EXPECTED_AFFECTED_ROWS: int = 1

# Id of a `Resource` with a duplicate pending draft.
UPDATE_RESOURCE_WITH_DUPLICATE_PENDING_DRAFT_RESOURCE_ID: int = 1

# Id of an approved `Resource` used for testing failure case.
UPDATE_RESOURCE_APPROVED_RESOURCE_ID: int = 3

# Id of DNE `Resource` for testing failure case.
UPDATE_RESOURCE_DNE_RESOURCE_ID: int = 99

# Duplicate `Resource` name used for testing failure case.
UPDATE_RESOURCE_DUPLICATE_RESOURCE_NAME: str = "Resource 2 Revision 1"

# Invalid `Resource` description used for testing failure case.
UPDATE_RESOURCE_INVALID_RESOURCE_DESCRIPTION: str = "Test Description."

# Malformed URL used for testing failure case.
UPDATE_RESOURCE_MALFORMED_RESOURCE_URL: str = "bad-url"

# Invalid thumbnail used for testing failure case.
UPDATE_RESOURCE_INVALID_RESOURCE_THUMBNAIL: float = 1234.245

# DNE `EmployeeLevel` ids used for testing failure case.
UPDATE_RESOURCE_EMPLOYEE_LEVEL_DNE_IDS: List[int] = [40, 50]

# DNE `SubFunction` ids used for testing failure case.
UPDATE_RESOURCE_SUBFUNCTION_DNE_IDS: List[int] = [60, 70]

# DNE `Tag` ids used for testing failure case.
UPDATE_RESOURCE_TAG_DNE_IDS: List[int] = [80, 90]

VALID_UPDATED_RESOURCE: dict = {
    "id": 2,
    "employee_levels": [
        {
            "id": 2,
            "name": "Manager",
            "description": "Manager Level 1.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "level": 2,
        }
    ],
    "subfunctions": [
        {
            "id": 1,
            "function": {
                "id": 1,
                "name": "Human Resources",
                "description": "Function 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "Training",
            "description": "Function 1 SubFunction 1.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
        }
    ],
    "tags": [
        {
            "id": 5,
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "label": "Engineering Tag",
        },
        {
            "id": 1,
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "label": "filter::site:Melbourne",
        },
    ],
    "primary_point_of_contact": "May.Parker@harris.com",
    "description": "Test resource description for update tests.",
    "uid": "2182c2ab-b3ab-444b-90fa-58a79031ae9c",
    "revision_number": None,
    "name": "Test Update Name.",
    "url": "https://www.test-site.com",
    "thumbnail": "/v1/media/resources/thumbnails/2182c2ab-b3ab-444b-90fa-58a79031ae9c/2024_03_01__18_00_00/resource_1.png",
    "type": "test update type",
    "download": False,
    "active": False,
    "previous_revision": 1,
    "created": "2025-03-01T13:00:00-05:00",
}
