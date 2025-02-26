"""
Arguments to be shared for QueryFilterState's update
controller pytests.
"""

# pylint: disable=line-too-long
from typing import List


# `QueryFilterState` id used for testing
# update.
UPDATE_QUERYFILTERSTATE_ID: int = 1

# `User` email used for testing update.
UPDATE_QUERYFILTERSTATE_USER_EMAIL: str = "May.Parker@harris.com"

# `Query` id used for testing update.
UPDATE_QUERYFILTERSTATE_QUERY_ID: int = 1

# `Function` ids used for updating a `QueryFilterState`
# record.
UPDATE_QUERYFILTERSTATE_FUNCTION_IDS: List[int] = [3, 4]

# `EmployeeLevel` ids used for updating a `QueryFilterState`
# record.
UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS: List[int] = [1, 2]

# `Tag` ids used for updating a `QueryFilterState`
# record.
UPDATE_QUERYFILTERSTATE_TAG_IDS: List[int] = [5, 6]

# `QueryFilterState` id that does not exist.
UPDATE_QUERYFILTERSTATE_ID_DNE: int = 20

# `User` email that does not exist.
UPDATE_QUERYFILTERSTATE_USER_EMAIL_DNE: str = "Test.UserDNE@harris.com"

# `User` email that does not match the
#  existing `QueryFilterState` record's user email.
UPDATE_QUERYFILTERSTATE_USER_EMAIL_DOES_NOT_MATCH: str = "Peter.Parker@harris.com"

# `Query` id that does not exist.
UPDATE_QUERYFILTERSTATE_QUERY_ID_DNE: int = 30

# `Function` ids that do not exist.
UPDATE_QUERYFILTERSTATE_FUNCTION_IDS_DNE: List[int] = [40, 50]

# `EmployeeLevel` ids that do not exist.
UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS_DNE: List[int] = [60, 70]

# `Tag` ids that do not exist.
UPDATE_QUERYFILTERSTATE_TAG_IDS_DNE: List[int] = [80, 90]

# Valid `QueryFilterState` record.
VALID_QUERYFILTERSTATE_RECORD: dict = {
    "id": 1,
    "search": {
        "id": 1,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@harris.com",
            "first_name": "May",
            "last_name": "Parker",
            "is_active": True,
        },
        "resources": [
            {
                "id": 1,
                "employee_levels": [
                    {
                        "id": 1,
                        "name": "Employee",
                        "description": "Employee Level 1.",
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                        "level": 1,
                    },
                    {
                        "id": 3,
                        "name": "Executive",
                        "description": "Executive Level 1.",
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                        "level": 3,
                    },
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
                    }
                ],
                "description": "A cinema resource.",
                "created": "2024-10-01T12:00:00-04:00",
                "uid": "d2ab62e8-4a0e-4b12-b94b-c128cae48222",
                "revision_number": 1,
                "name": "Resource 1 Revision 1",
                "url": "example-revision-site.org",
                "thumbnail": "/v1/media/resources/thumbnails/d2ab62e8-4a0e-4b12-b94b-c128cae48222/2024_10_01__16_00_00/resource_1.png",
                "primary_point_of_contact": "May.Parker@harris.com",
                "type": "Resource Type 1",
                "download": False,
                "active": True,
                "previous_revision": None,
            }
        ],
        "created": "2024-10-01T12:00:00-04:00",
        "search_term": "cinema",
    },
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "functions": [3, 4],
    "employee_levels": [1, 2],
    "tags": [5, 6],
    "created": "2024-10-01T12:00:00-04:00",
}
