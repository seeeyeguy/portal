"""
Arguments to be shared for Resource's create
controller pytests.
"""

from typing import List

from django.core.files.base import File

from directory.controllers.Resource.Resource import CreateResourceParams

# pylint: disable=line-too-long

# `User` email used when testing `Resource` create view.
CREATE_RESOURCE_USER_EMAIL: str = "May.Parker@harris.com"

# `User` email used when testing `Resource` create with a
# `User` that does not have `Access` with a valid `Role`.
CREATE_RESOURCE_USER_EMAIL_INVALID_ROLE: str = "Gwen.Stacy@harris.com"

# `User` email used when testing `Resource` create with a
# `User` that does not have `Access` to create a `Resource`
# within a set of given `SubFunction`s.
CREATE_RESOURCE_USER_EMAIL_SUBFUNCTIONS_PERMISSIONS_DENIED: str = (
    "Miles.Morales@harris.com"
)

# Base parameters used for successful `Resource` creation.
BASE_CREATE_RESOURCE_STRUCTURE_PARAMS: CreateResourceParams = {
    "uid": None,
    "previous_revision": None,
    "name": "Test Create Name",
    "description": "Test resource description for create tests.",
    "url": "https://www.test-site.com",
    "thumbnail": File(b""),  # type: ignore[typeddict-item,unused-ignore,arg-type]
    "employee_levels": [3],
    "subfunctions": [2, 5],
    "tags": [1, 2, 3],
    "point_of_contacts": ["May.Parker@harris.com"],
    "type": "test create type",
    "download": False,
}

# Base parameters used for succesful `Resource` revision creation.
BASE_CREATE_RESOURCE_REVISION_STRUCTURE_PARAMS: CreateResourceParams = {
    "uid": "4878469f-6d52-46da-aee3-77905002cd12",
    "previous_revision": 1,
    "name": "Resource 1 Revision 2",
    "description": "Resource 1 Revision 2 description.",
    "url": "https://www.example-resource-1-revision-2.org",
    "thumbnail": File(b""),  # type: ignore[typeddict-item,unused-ignore,arg-type]
    "employee_levels": [3],
    "subfunctions": [2, 5],
    "tags": [1, 2, 3],
    "point_of_contacts": ["May.Parker@harris.com"],
    "type": "resource type 1",
    "download": False,
}

# Base parameters used for successful `Resource` creation (JSON serializable).
BASE_CREATE_RESOURCE_STRUCTURE_PARAMS_JSON_SERIALIZABLE = {
    **BASE_CREATE_RESOURCE_STRUCTURE_PARAMS,
    "thumbnail": None,
}

# Base parameters used for successful `Resource` revision creation (JSON serializable).
BASE_CREATE_RESOURCE_REVISION_STRUCTURE_PARAMS_JSON_SERIALIZABLE = {
    **BASE_CREATE_RESOURCE_REVISION_STRUCTURE_PARAMS,
    "thumbnail": None,
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

# DNE `Access` `User` emails for `PointOfContact`s used for testing failure case.
CREATE_RESOURCE_POINT_OF_CONTACT_EMAILS_DNE: List[str] = [
    "May.Parker@harris.com",
    "DNE.User@harris.com",
]

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
    "primary_point_of_contact": "May.Parker@harris.com",
    "revision_number": None,
    "name": "Test Create Name",
    "description": "Test resource description for create tests.",
    "url": "https://www.test-site.com",
    "thumbnail": None,
    "type": "test create type",
    "download": False,
    "active": False,
    "previous_revision": None,
}

VALID_CREATED_RESOURCE_REVISION: dict = {
    "id": 5,
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
    "primary_point_of_contact": "May.Parker@harris.com",
    "uid": "4878469f-6d52-46da-aee3-77905002cd12",
    "revision_number": None,
    "name": "Resource 1 Revision 2",
    "description": "Resource 1 Revision 2 description.",
    "url": "https://www.example-resource-1-revision-2.org",
    "thumbnail": None,
    "type": "resource type 1",
    "download": False,
    "active": False,
    "previous_revision": 1,
}
