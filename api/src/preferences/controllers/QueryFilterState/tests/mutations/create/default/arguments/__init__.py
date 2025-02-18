"""
Arguments to be shared for QueryFilterState's create
controller pytests.
"""

from typing import List

# Arguments for successfully creating `QueryFilterState` record.
CREATE_QUERY_FILTER_STATE_USER: str = "May.Parker@harris.com"
CREATE_QUERY_FILTER_STATE_QUERY_ID: int = 1
CREATE_QUERY_FILTER_STATE_FUNCTION_IDS: List[int] = [1]
CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS: List[int] = [1]
CREATE_QUERY_FILTER_STATE_TAG_IDS: List[int] = [1]

# Invalid `User` email for testing failure case.
CREATE_QUERY_FILTER_STATE_USER_DNE: str = "Fake.User@harris.com"

# Invalid `Query` id for testing failure case.
CREATE_QUERY_FILTER_STATE_QUERY_ID_DNE: int = 9999

# Invalid `Function` id for testing failure case.
CREATE_QUERY_FILTER_STATE_FUNCTION_ID_DNE: List[int] = [9999]

# Invalid `EmployeeLevel` id for testing failure case.
CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_ID_DNE: List[int] = [9999]

# Invalid `Tag` id for testing failure case.
CREATE_QUERY_FILTER_STATE_TAG_ID_DNE: List[int] = [9999]

# Expected values for created `QueryFilterState`.
VALID_CREATED_QUERY_FILTER_STATE: dict = {
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
                        "id": 1,
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                        "label": "filter::site:Melbourne",
                    }
                ],
                "description": "Resource 1 Revision 1 description.",
                "created": "2024-10-01T12:00:00-04:00",
                "uid": "fa1d4316-3d9a-44be-950e-7cb0b88f49f8",
                "revision_number": 1,
                "name": "Resource 1 Revision 1",
                "url": "example-site.org",
                "thumbnail": "/v1/media/resources/thumbnails/fa1d4316-3d9a-44be-950e-7cb0b88f49f8/1/resource_1.png",
                "primary_point_of_contact": "May.Parker@harris.com",
                "type": "Resource Type 1",
                "download": False,
                "active": True,
                "previous_revision": None,
            }
        ],
        "created": "2024-10-01T12:00:00-04:00",
        "search_term": "Resource 1",
    },
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "functions": [1],
    "employee_levels": [1],
    "tags": [1],
}
