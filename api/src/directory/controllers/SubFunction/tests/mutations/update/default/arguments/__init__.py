"""
Arguments to be shared for SubFunction's update
controller pytests.
"""

# Arguments used for testing the successful update of a `SubFunction` record.
UPDATE_SUBFUNCTION_ID: int = 1
UPDATE_SUBFUNCTION_NAME: str = "Test Update SubFunction Name"
UPDATE_SUBFUNCTION_DESCRIPTION: str = "Test Update SubFunction Description."
UPDATE_SUBFUNCTION_FUNCTION_ID: int = 2

# `Function` id used for testing failure case of DNE `Function` record.
UPDATE_SUBFUNCTION_FUNCTION_ID_DNE: int = 99

# `SubFunction` id used for testing failure case of DNE `SubFunction` record.
UPDATE_SUBFUNCTION_ID_DNE: int = 999

# Duplicate `SubFunction` name string used for failure case.
UPDATE_SUBFUNCTION_DUPLICATE_NAME: str = "Recruiting"

# Number of expected `SubFunction` records to be affected after a
# successful update.
UPDATE_SUBFUNCTION_EXPECTED_ROWS_AFFECTED: int = 1

# Expected `SubFunction`values expected after updating.
VALID_SUBFUNCTION: dict = {
    "id": 1,
    "function": {
        "id": 2,
        "name": "Engineering",
        "description": "Function 2.",
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
    "name": "Test Update SubFunction Name",
    "description": "Test Update SubFunction Description.",
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
}
