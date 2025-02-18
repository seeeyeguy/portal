"""
Arguments to be shared for EmployeeLevel's create
controller pytests.
"""

# `User` email used for testing create with a superuser.
CREATE_EMPLOYEELEVEL_USER_EMAIL_SUPERUSER: str = "Tony.Stark@harris.com"

# `User` email used for testing create with a nonsuperuser.
CREATE_EMPLOYEELEVEL_USER_EMAIL_NONSUPERUSER: str = "May.Parker@harris.com"

# Arguments for successfully creating `EmployeeLevel` record.
CREATE_EMPLOYEELEVEL_NAME = "Successful Employee Level"
CREATE_EMPLOYEELEVEL_DESCRIPTION = "This is a test EmployeeLevel"
CREATE_EMPLOYEELEVEL_LEVEL = 4

# Arguments for duplicate values when creating `EmployeeLevel` record.
CREATE_EMPLOYEELEVEL_NAME_DUPLICATE = "Executive"
CREATE_EMPLOYEELEVEL_LEVEL_DUPLICATE = 3

# Expected values for created `EmployeeLevel`.
CREATE_EMPLOYEELEVEL_EXPECTED_VALUES: dict = {
    "id": 4,
    "name": "Successful Employee Level",
    "description": "This is a test EmployeeLevel",
    "level": 4,
}
