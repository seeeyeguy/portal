"""
Arguments to be shared for Query's create
controller pytests.
"""

# `User` email used for testing create `Query`.
CREATE_QUERY_USER_EMAIL: str = "May.Parker@harris.com"

# `User` DNE email used for testing failure case.
CREATE_QUERY_USER_EMAIL_DNE: str = "non.existing.user@harris.com"

# Search term used for testing create `Query`.
CREATE_QUERY_SEARCH_TERM: str = "Resource"

# Search term that yields no results.
SEARCH_TERM_NO_RESULTS: str = "non_existent_term"

# Valid `Query` to validate creation.
VALID_CREATED_QUERY: dict = {
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
            "description": "popstick.",
            "created": "2024-08-27T12:00:00-04:00",
            "uid": "f6a31db2-5271-401a-901e-9220e0e4cda2",
            "revision_number": 1,
            "name": "Resource 1 Revision 1",
            "url": "example.org",
            "thumbnail": "/v1/media/resources/thumbnails/f6a31db2-5271-401a-901e-9220e0e4cda2/2024_08_27__16_00_00/resource_1.png",
            "primary_point_of_contact": "May.Parker@harris.com",
            "type": "Resource Type 1",
            "download": False,
            "active": True,
            "previous_revision": None,
        },
        {
            "id": 2,
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
            "description": "ripstick.",
            "created": "2024-08-27T12:00:00-04:00",
            "uid": "2ca5ca29-5dbb-4333-99d3-750e30b1ed48",
            "revision_number": 1,
            "name": "Resource 2 Revision 1",
            "url": "example.gov",
            "thumbnail": "/v1/media/resources/thumbnails/2ca5ca29-5dbb-4333-99d3-750e30b1ed48/2024_08_27__16_00_00/resource_2.png",
            "primary_point_of_contact": "May.Parker@harris.com",
            "type": "Resource Type 2",
            "download": False,
            "active": True,
            "previous_revision": None,
        },
    ],
    "search_term": "Resource",
}

# Valid `Query` with no results.
VALID_NO_RESULTS_QUERY: dict = {
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "resources": [],
    "search_term": "non_existent_term",
}
