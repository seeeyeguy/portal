"""
Arguments to be shared for EmployeeLevel's delete
controller pytests.
"""

# User for deleting a `EmployeeLevel` record.
DELETE_EMPLOYEE_LEVEL_USER_EMAIL: str = "Tony.Stark@harris.com"

# Id used to test deleting by `EmployeeLevel` id.
DELETE_EMPLOYEE_LEVEL_BY_ID: int = 1

# Valid `EmployeeLevel` record dictionary.
VALID_EMPLOYEELEVEL_RECORDS: dict = {
    "id": 1,
    "name": "Employee",
    "description": "Employee Level 1.",
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
    "level": 1,
}
