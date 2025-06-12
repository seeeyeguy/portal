"""
Arguments to be shared for QueryFilterState's fetch
controller pytests.
"""

# pylint: disable=line-too-long

# `User` email used for testing fetch.
FETCH_QUERYFILTERSTATE_USER_EMAIL: str = "May.Parker@harris.com"

# `User` email that does not exist.
FETCH_QUERYFILTERSTATE_USER_EMAIL_DNE: str = "Test.User.DNE@harris.com"

# `User` email that does not have an associated `QueryFilterState`.
FETCH_QUERYFILTERSTATE_QUERYFILTERSTATE_DNE_USER_EMAIL: str = "Peter.Parker@harris.com"

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
                        "id": 2,
                        "name": "Manager",
                        "description": "Manager Level 1.",
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                        "level": 2,
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
                        "id": 7,
                        "function": {
                            "id": 4,
                            "name": "Operations",
                            "description": "Function 4.",
                            "created": "2024-08-27T12:00:00-04:00",
                            "modified": "2024-08-27T12:00:00-04:00",
                        },
                        "name": "Quality",
                        "description": "Function 4 SubFunction 1.",
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                    },
                    {
                        "id": 3,
                        "function": {
                            "id": 2,
                            "name": "Engineering",
                            "description": "Function 2.",
                            "created": "2024-08-27T12:00:00-04:00",
                            "modified": "2024-08-27T12:00:00-04:00",
                        },
                        "name": "Software Engineering",
                        "description": "Function 2 SubFunction 1.",
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                    },
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
                    },
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
                    {
                        "id": 2,
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                        "label": "filter::site:Rochester",
                    },
                    {
                        "id": 4,
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                        "label": "restricted::department:Imaging",
                    },
                ],
                "description": "A cinematic universe film resource.",
                "created": "2024-10-01T12:00:00-04:00",
                "uid": "6b6289bf-0e89-4edf-9eb8-4db57184ae42",
                "revision_number": 1,
                "name": "Resource 1 Revision 1",
                "url": "example-revision-site-1.org",
                "thumbnail": "/v1/media/resources/thumbnails/6b6289bf-0e89-4edf-9eb8-4db57184ae42/2024_10_01__16_00_00/resource_1.png",
                "primary_point_of_contact": "May.Parker@harris.com",
                "type": "Resource Type 1",
                "download": False,
                "active": True,
                "deleted": False,
                "previous_revision": None,
            }
        ],
        "created": "2024-10-01T12:00:00-04:00",
        "search_term": "universe",
    },
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "functions": [2, 1],
    "employee_levels": [3],
    "tags": [2],
    "created": "2024-10-01T12:00:00-04:00",
    "modified": "2024-10-01T12:00:00-04:00",
}
