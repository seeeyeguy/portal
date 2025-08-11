"""
Arguments to be shared for Access's revoke update
controller pytests.
"""

REVOKE_ACCESS_ADMIN_USER_EMAIL: str = "Tony.Stark@harris.com"

REVOKE_ACCESS_NON_ADMIN_USER_EMAIL: str = "Peter.Parker@harris.com"

REVOKE_ACCESS_ACCESS_ID: int = 3
REVOKE_ACCESS_EXPECTED_ROWS_AFFECTED: int = 1

REVOKE_ACCESS_ACCESS_ID_DNE: int = 99

REVOKE_ACCESS_ADMIN_ACCESS_ID: int = 1

REVOKED_ACCESS_EXPECTED_ACCESS: dict = {
    "id": 3,
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "role": {
        "id": 3,
        "created": "2024-08-27T12:00:00-04:00",
        "name": "Data Steward",
        "description": "Data Steward.",
        "level": 3,
    },
    "stage": [],
    "access_granted_date": "2024-08-27T12:00:00-04:00",
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
            "id": 6,
            "function": {
                "id": 3,
                "name": "Finance",
                "description": "Function 3.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "Cost Planning",
            "description": "Function 3 SubFunction 2.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
        },
        {
            "id": 8,
            "function": {
                "id": 4,
                "name": "Operations",
                "description": "Function 4.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "General",
            "description": "Function 4 SubFunction 2.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
        },
        {
            "id": 4,
            "function": {
                "id": 2,
                "name": "Engineering",
                "description": "Function 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "Mechanical Engineering",
            "description": "Function 2 SubFunction 2.",
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
}
