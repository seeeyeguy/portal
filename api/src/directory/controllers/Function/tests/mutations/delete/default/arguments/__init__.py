"""
Arguments to be shared for Function's delete
controller pytests.
"""

# Id used for testing delete by function id
# tests.
DELETE_FUNCTION_BY_ID: int = 1

# `User` email used for testing delete `Function` record.
DELETE_FUNCTION_USER_EMAIL: str = "Tony.Stark@harris.com"

# Expected number of rows affected from the database, after
# deleting `Function` record.
DELETE_FUNCTION_AFFECTED_FUNCTION_ROWS: int = 1
DELETE_FUNCTION_AFFECTED_SUBFUNCTION_ROWS_RELATED_TO_FUNCTION: int = 2
DELETE_FUNCTION_AFFECTED_ACCESS_ROWS_RELATED_TO_SUBFUNCTIONS_AND_FUNCTION: int = 4
DELETE_FUNCTION_ROWS_AFFECTED: int = (
    DELETE_FUNCTION_AFFECTED_FUNCTION_ROWS
    + DELETE_FUNCTION_AFFECTED_SUBFUNCTION_ROWS_RELATED_TO_FUNCTION
    + DELETE_FUNCTION_AFFECTED_ACCESS_ROWS_RELATED_TO_SUBFUNCTIONS_AND_FUNCTION
)

# Valid `Function` record dictionary.
VALID_FUNCTION_RECORDS: dict = {
    "id": 1,
    "name": "Human Resources",
    "description": "Function 1.",
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
}
