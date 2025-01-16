"""
Arguments to be shared for Function's create
controller pytests.
"""

# Arguments for successfully creating `Function` record.
CREATE_FUNCTION_NAME: str = "Create Function"
CREATE_FUNCTION_DESCRIPTION: str = "Create Function Level 1."

# Duplicate `Function` name for testing failure case.
CREATE_FUNCTION_DUPLICATE_NAME: str = "Engineering"

# Expected values for created `Function`.
CREATE_FUNCTION_EXPECTED_VALUES: dict = {
    "name": "Create Function",
    "description": "Create Function Level 1.",
}
