"""
Arguments to be shared for Function's update
controller pytests.
"""

# User for updating the `Function` record.
UPDATE_FUNCTION_USER_EMAIL: str = "Tony.Stark@harris.com"

# Arguments for successfully updating `Function` record.
UPDATE_FUNCTION_ID: int = 1
UPDATE_FUNCTION_NAME: str = "Update Function"
UPDATE_FUNCTION_DESCRIPTION: str = "Update Function Level 1."

# Duplicate `Function` name for testing failure case.
UPDATE_FUNCTION_DUPLICATE_NAME: str = "Human Resources"

# Duplicate `Function` id for testing failure case.
UPDATE_FUNCTION_ID_DUPLICATE: int = 2

# Invalid `Function` id for testing failure case.
UPDATE_FUNCTION_ID_DNE: int = 9999

# Expected values for updated `Function`.
UPDATE_FUNCTION_EXPECTED_VALUES: dict = {
    "id": 1,
    "name": "Update Function",
    "description": "Update Function Level 1.",
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
}
