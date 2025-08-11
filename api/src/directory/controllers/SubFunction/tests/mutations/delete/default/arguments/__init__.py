"""
Arguments to be shared for SubFunction's delete
controller pytests.
"""

# Email used to test deleting a `SubFunction` record.
DELETE_SUBFUNCTION_USER_EMAIL = "Tony.Stark@harris.com"

# `SubFunction` id used for testing success case.
DELETE_SUBFUNCTION_SUBFUNCTION_ID: int = 2

# Expected number of rows affected from the database, after
# deleting the `SubFunction` record.
DELETE_SUBFUNCTION_AFFECTED_SUBFUNCTION_ROWS: int = 1
DELETE_SUBFUNCTION_AFFECTED_ACCESS_ROWS_RELATED_TO_SUBFUNCTION: int = 2
DELETE_SUBFUNCTION_ROWS_AFFECTED: int = (
    DELETE_SUBFUNCTION_AFFECTED_SUBFUNCTION_ROWS
    + DELETE_SUBFUNCTION_AFFECTED_ACCESS_ROWS_RELATED_TO_SUBFUNCTION
)
