"""
Arguments to be shared for Tag's delete
controller pytests.
"""

# Id used for testing delete by Tag id tests.
DELETE_TAG_BY_ID: int = 1

# `User` email used for testing delete `Tag` record.
DELETE_TAG_USER_EMAIL: str = "May.Parker@harris.com"

# Valid `Tag` record dictionary.
VALID_TAG_RECORDS: dict = {
    "id": 1,
    "label": "filter::site:Melbourne",
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
}
