"""
Arguments to be shared for Favorite's fetch
controller pytests.
"""

from typing import List

# `User` email used for testing fetching user `Favorite`(s).
FETCH_FAVORITE_USER_EMAIL: str = "May.Parker@harris.com"

# `User` DNE email used for testing failure case.
FETCH_FAVORITE_USER_EMAIL_DNE: str = "DNE.User@harris.com"

# List of serialized `Favorite`s to validate
# results from the fetch.
VALID_FAVORITES: List[dict] = [
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@harris.com",
            "first_name": "May",
            "last_name": "Parker",
            "is_active": True,
        },
        "resource": {
            "id": 1,
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
                }
            ],
            "tags": [
                {
                    "id": 6,
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                    "label": "Operations Tag",
                }
            ],
            "description": "Test Resource 1.",
            "created": "2025-01-01T11:00:00-05:00",
            "uid": "cdd9478d-a77a-42c1-9995-2c78ff176955",
            "revision_number": 1,
            "name": "Resource 1 Revision 1",
            "url": "example-resource-1.org",
            "thumbnail": "/v1/media/resources/thumbnails/cdd9478d-a77a-42c1-9995-2c78ff176955/1/resource_1.png",
            "primary_point_of_contact": "May.Parker@harris.com",
            "type": "Resource Type 1",
            "download": False,
            "active": True,
            "previous_revision": None,
        },
        "rank": 1,
        "created": "2025-01-02T11:00:00-05:00",
    },
    {
        "id": 2,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@harris.com",
            "first_name": "May",
            "last_name": "Parker",
            "is_active": True,
        },
        "resource": {
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
                }
            ],
            "tags": [
                {
                    "id": 4,
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                    "label": "restricted::department:Imaging",
                }
            ],
            "description": "Test Resource 2.",
            "created": "2025-01-01T11:00:00-05:00",
            "uid": "f2c533c4-7ee2-4a0b-9e31-6ce8d826d522",
            "revision_number": 1,
            "name": "Resource 2 Revision 1",
            "url": "example-resource-2.org",
            "thumbnail": "/v1/media/resources/thumbnails/f2c533c4-7ee2-4a0b-9e31-6ce8d826d522/2/resource_2.png",
            "primary_point_of_contact": "May.Parker@harris.com",
            "type": "Resource Type 2",
            "download": False,
            "active": True,
            "previous_revision": None,
        },
        "rank": 2,
        "created": "2024-01-02T11:00:00-05:00",
    },
]
