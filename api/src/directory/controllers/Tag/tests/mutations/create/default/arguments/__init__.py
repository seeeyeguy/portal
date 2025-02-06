"""
Arguments to be shared for Tag's create
controller pytests.
"""

# Arguments for successfully creating `Tag` record.
CREATE_TAG_LABEL: str = "Create Tag"

# `User` email used for testing create `Tag`.
CREATE_TAG_USER_EMAIL: str = "Peter.Parker@harris.com"

# Duplicate `Tag` label for testing failure case.
CREATE_DUPLICATE_TAG: str = "filter::site:Melbourne"

# Expected value for created `Tag`.
CREATE_TAG_EXPECTED_VALUE: dict = {"label": "Create Tag"}
