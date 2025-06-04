"""
Arguments to be shared for Access's update
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
    "subfunctions": [5, 6, 8, 4, 7, 2, 3, 1],
}
