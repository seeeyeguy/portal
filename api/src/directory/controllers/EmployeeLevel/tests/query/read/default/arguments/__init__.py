"""
Arguments to be shared for EmployeeLevels's fetch
controller pytests.
"""

# Valid `EmployeeLevel` ids.
EMPLOYEELEVEL_ID_1: int = 1
EMPLOYEELEVEL_ID_2: int = 2
EMPLOYEELEVEL_ID_3: int = 3

# Id used for testing fetch by employee level id
# tests.
FETCH_EMPLOYEELEVEL_BY_ID: int = 2

# Id used for testing fetch by employee level id
# DNE tests.
FETCH_EMPLOYEELEVEL_BY_ID_DNE: int = 999

# Valid `EmployeeLevel` records dictionary.
VALID_EMPLOYEELEVEL_RECORDS: dict = {
    EMPLOYEELEVEL_ID_1: {
        "id": 1,
        "name": "Employee",
        "description": "Employee Level 1.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "level": 1,
    },
    EMPLOYEELEVEL_ID_2: {
        "id": 2,
        "name": "Manager",
        "description": "Manager Level 1.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "level": 2,
    },
    EMPLOYEELEVEL_ID_3: {
        "id": 3,
        "name": "Executive",
        "description": "Executive Level 1.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "level": 3,
    },
}
