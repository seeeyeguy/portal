"""
Arguments to be shared for SubFunction's create
controller pytests.
"""

# Arguments for successfully creating `SubFunction` record.
CREATE_SUBFUNCTION_NAME: str = "Create Subfunction."
CREATE_SUBFUNCTION_DESCRIPTION: str = "Create SubFunction Level 1."
CREATE_SUBFUNCTION_FUNCTION_ID: int = 3

# `User` email used for testing login verification on views
# when creating `SubFunction` record.
CREATE_SUBFUNCTION_USER_EMAIL: str = "Tony.Stark@harris.com"

# Duplicate `SubFunction` name for testing failure case.
CREATE_SUBFUNCTION_DUPLICATE_NAME: str = "Cost Planning"

# Invalid `Function` id for testing failure case.
CREATE_SUBFUNCTION_FUNCTION_DNE: int = 9999

# Expected values for created `SubFunction`.
CREATE_SUBFUNCTION_EXPECTED_VALUES: dict = {
    "function": {
        "id": 3,
        "name": "Finance",
        "description": "Function 3.",
    },
    "name": "Create Subfunction.",
    "description": "Create SubFunction Level 1.",
}
