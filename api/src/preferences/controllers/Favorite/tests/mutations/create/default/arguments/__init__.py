"""
Arguments to be shared for Favorite's create
controller pytests.
"""

# Arguments for successfully creating `Favorite` record.
CREATE_FAVORITE_USER: str = "May.Parker@harris.com"
CREATE_FAVORITE_RESOURCE_ID: int = 3

# Invalid `User` email for testing failure case.
CREATE_FAVORITE_USER_DNE: str = "DNE.User@harris.com"

# Invalid `Resource` id for testing failure case.
CREATE_FAVORITE_RESOURCE_DNE: int = 9999

# `Resource` id for testing creating `Favorite` that already exists.
CREATE_FAVORITE_EXISTING_FAVORITE_RESOURCE_ID: int = 2

# `Resource` id for testing creating `Favorite` with inactive `Resource`.
CREATE_FAVORITE_INACTIVE_RESOURCE_ID: int = 4

# Expected values for created `Favorite`.
CREATE_FAVORITE_EXPECTED_VALUES: dict = {
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@l3harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "resource": {
        "id": 3,
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
        ],
        "description": "Resource 3 description.",
        "created": "2024-08-27T12:00:00-04:00",
        "uid": "a157e2a8-1db7-4ef2-adc1-90e109af0557",
        "revision_number": 1,
        "name": "Resource 3",
        "url": "example-3.org",
        "thumbnail": "/v1/media/resources/thumbnails/a157e2a8-1db7-4ef2-adc1-90e109af0557/2024_08_27__16_00_00/resource_3.png",
        "primary_point_of_contact": "May.Parker@l3harris.com",
        "type": "Resource Type 3",
        "download": False,
        "active": True,
        "deleted": False,
        "previous_revision": None,
    },
    "rank": 3,
}
