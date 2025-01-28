"""
Arguments to be shared for SubFunction's delete
controller pytests.
"""

# Email used to test deleting a `SubFunction` record.
DELETE_SUBFUNCTION_USER_EMAIL = "May.Parker@harris.com"

# `SubFunction` id used for testing success case.
DELETE_SUBFUNCTION_SUBFUNCTION_ID: int = 2

# Expected number of rows deleted from the database.
DELETE_SUBFUNCTION_ROWS_AFFECTED: int = 1
