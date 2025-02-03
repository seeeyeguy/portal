"""
Arguments to be shared for Tag's update
controller pytests.
"""

# `User` email used for testing update.
UPDATE_TAG_USER_EMAIL: str = "Tony.Stark@harris.com"

# Arguments for successfully updating `Tag` record.
UPDATE_TAG_ID: int = 4
UPDATE_TAG_LABEL: str = "Space and Airborne Tag"

# Arguments for failing to update `Tag` record with 'tag_id' that does not exist.
UPDATE_TAG_ID_DNE: int = 50

# Arguments for failing to update `Tag` record with duplicate 'label'.
UPDATE_TAG_LABEL_DUPLICATE: str = "Finance Tag"

# Expected values for updated `Tag`.
UPDATE_TAG_EXPECTED_VALUES: dict = {"id": 4, "label": "Space and Airborne Tag"}
