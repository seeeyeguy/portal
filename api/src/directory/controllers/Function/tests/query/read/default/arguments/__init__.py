"""
Arguments to be shared for Function's fetch
controller pytests.
"""

# Valid `Function` ids.
FUNCTION_ID_1: int = 1
FUNCTION_ID_2: int = 2
FUNCTION_ID_3: int = 3
FUNCTION_ID_4: int = 4

# Id used for testing fetch by function id
# tests.
FETCH_FUNCTION_BY_ID: int = 4

# Id used for testing fetch by function id
# DNE tests.
FETCH_FUNCTION_BY_ID_DNE: int = 99

# Valid `Function` records dictionary.
VALID_FUNCTION_RECORDS: dict = {
    FUNCTION_ID_1: {
        "id": 1,
        "name": "Human Resources",
        "description": "Function 1.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
    FUNCTION_ID_2: {
        "id": 2,
        "name": "Engineering",
        "description": "Function 2.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
    FUNCTION_ID_3: {
        "id": 3,
        "name": "Finance",
        "description": "Function 3.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
    FUNCTION_ID_4: {
        "id": 4,
        "name": "Operations",
        "description": "Function 4.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
}
