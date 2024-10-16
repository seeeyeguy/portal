"""
Arguments to be shared for SubFunction's fetch
controller pytests.
"""

# Valid `SubFunction` ids.
SUBFUNCTION_ID_1: int = 1
SUBFUNCTION_ID_2: int = 2
SUBFUNCTION_ID_3: int = 3
SUBFUNCTION_ID_4: int = 4
SUBFUNCTION_ID_5: int = 5
SUBFUNCTION_ID_6: int = 6
SUBFUNCTION_ID_7: int = 7
SUBFUNCTION_ID_8: int = 8


# Id used for testing fetch by subfunction id
# tests.
FETCH_SUBFUNCTION_BY_ID: int = 4

# Id used for testing fetch by subfunction id
# DNE tests.
FETCH_SUBFUNCTION_BY_ID_DNE: int = 99

# Valid `SubFunction` records dictionary.
VALID_SUBFUNCTION_RECORDS: dict = {
    SUBFUNCTION_ID_1: {
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
    SUBFUNCTION_ID_2: {
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
    SUBFUNCTION_ID_3: {
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
    SUBFUNCTION_ID_4: {
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
    SUBFUNCTION_ID_5: {
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
    SUBFUNCTION_ID_6: {
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
    SUBFUNCTION_ID_7: {
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
    SUBFUNCTION_ID_8: {
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
}
