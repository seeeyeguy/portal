"""
Arguments to be shared for Resource's create
controller pytests.
"""

from typing import List

from directory.controllers.Resource.Resource import CreateResourceParams

# pylint: disable=line-too-long

# Base parameters used for successful `Resource` creation.
BASE_CREATE_RESOURCE_STRUCTURE_PARAMS: CreateResourceParams = {
    "uid": "66d4baed-9d6e-4167-9ad1-a62f8492cf32",
    "previous_revision": None,
    "name": "Test Create Name",
    "description": "Test resource description for create tests.",
    "url": "https://www.test-site.com",
    "thumbnail": None,  # type: ignore[typeddict-item,unused-ignore]
    "employee_levels": [3],
    "subfunctions": [2, 5],
    "tags": [1, 2, 3],
    "type": "test create type",
    "download": False,
}

# Id for a `Resource's` previous revision does not exist used for testing failure case.
CREATE_RESOURCE_PREVIOUS_RESOURCE_REVISION_DNE_ID: int = 999

# Pending draft `Resource` uid used for testing failure case.
CREATE_RESOURCE_WITH_DUPLICATE_PENDING_DRAFT_RESOURCE_ID: str = (
    "aa852d37-938d-4b81-8db9-b1163b286619"
)

# Previous revision `Resource` id used for testing failure case.
CREATE_RESOURCE_PREVIOUS_RESOURCE_REVISION_ID: int = 2

# Duplicate `Resource` name used for testing failure case.
CREATE_RESOURCE_DUPLICATE_RESOURCE_NAME: str = "Resource 1 Revision 1"

# Invalid `Resource` description used for testing failure case.
CREATE_RESOURCE_INVALID_RESOURCE_DESCRIPTION: str = "Test Description."

# Malformed URL used for testing failure case.
CREATE_RESOURCE_MALFORMED_RESOURCE_URL: str = "incorrect-url"

# Invalid thumbnail used for testing failure case.
CREATE_RESOURCE_INVALID_RESOURCE_THUMBNAIL: float = 5280.54

# DNE `EmployeeLevel` ids used for testing failure case.
CREATE_RESOURCE_EMPLOYEE_LEVEL_DNE_IDS: List[int] = [40, 50]

# DNE `Subfunction` ids used for testing failure case.
CREATE_RESOURCE_SUBFUNCTION_DNE_IDS: List[int] = [60, 70]

# DNE `Tag` ids used for testing failure case.
CREATE_RESOURCE_TAG_DNE_IDS: List[int] = [80, 90]

VALID_CREATED_RESOURCE: dict = {
    "id": 4,
    "employee_levels": [
        {
            "id": 3,
            "name": "Executive",
            "description": "Executive Level 1.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "level": 3,
        }
    ],
    "subfunctions": [
        {
            "id": 5,
            "function": {
                "id": 3,
                "name": "Finance",
                "description": "Function 3.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "Capital",
            "description": "Function 3 SubFunction 1.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
        },
        {
            "id": 2,
            "function": {
                "id": 1,
                "name": "Human Resources",
                "description": "Function 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "Recruiting",
            "description": "Function 1 SubFunction 2.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
        },
    ],
    "tags": [
        {
            "id": 1,
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "label": "filter::site:Melbourne",
        },
        {
            "id": 2,
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "label": "filter::site:Rochester",
        },
        {
            "id": 3,
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
            "label": "restricted::department:GeoSpatial",
        },
    ],
    "primary_point_of_contact": None,
    "description": "Test resource description for create tests.",
    "revision_number": None,
    "name": "Test Create Name",
    "url": "https://www.test-site.com",
    "thumbnail": None,
    "type": "test create type",
    "download": False,
    "active": False,
    "previous_revision": None,
}
