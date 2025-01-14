"""
Arguments to be shared for Function's delete
controller pytests.
"""

# Id used for testing delete by function id
# tests.
DELETE_FUNCTION_BY_ID: int = 1

# `User` email used for testing delete `Function` record.
DELETE_FUNCTION_USER_EMAIL: str = "May.Parker@harris.com"

# Valid `Function` record dictionary.
VALID_FUNCTION_RECORDS: dict = {
    "id": 1,
    "name": "Human Resources",
    "description": "Function 1.",
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
}
