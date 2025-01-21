"""
Arguments to be shared for EmployeeLevel's update
controller pytests.
"""

# Arguments for successfully updating `EmployeeLevel` record.
UPDATE_EMPLOYEELEVEL_ID: int = 1
UPDATE_EMPLOYEELEVEL_NAME: str = "Update Employee"
UPDATE_EMPLOYEELEVEL_DESCRIPTION: str = "Update Employee Level 1."

# `User` email used for testing update.
UPDATE_EMPLOYEELEVEL_USER_EMAIL: str = "May.Parker@harris.com"

# Duplicate `EmployeeLevel` name for testing failure case.
UPDATE_EMPLOYEELEVEL_DUPLICATE_NAME: str = "Manager"

# Invalid `EmployeeLevel` id and name for testing failure case.
UPDATE_EMPLOYEELEVEL_DNE: int = 9999
UPDATE_EMPLOYEELEVEL_NAME_DNE: str = "Employee Level DNE"

# Expected values for updated `EmployeeLevel`.
UPDATE_EMPLOYEELEVEL_EXPECTED_VALUES: dict = {
    "id": 1,
    "name": "Update Employee",
    "description": "Update Employee Level 1.",
    "level": 1,
}
