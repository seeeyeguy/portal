"""
Arguments to be shared for Tag's fetch
controller pytests.
"""

from typing import List

# Valid `Tag` ids.
TAG_ID_1: int = 1
TAG_ID_2: int = 2
TAG_ID_3: int = 3
TAG_ID_4: int = 4
TAG_ID_5: int = 5
TAG_ID_6: int = 6
TAG_ID_7: int = 7
TAG_ID_8: int = 8

# Id used for testing fetch by tag id
# tests.
FETCH_TAG_BY_ID: int = 5

# Page number used in testing fetch tag
# with page tests.
FETCH_TAG_WITH_PAGE: int = 1

# Page number that exceeds the number of
# pages used in testing fetch tag with
# page tests.
FETCH_TAG_WITH_PAGE_EXCEEDING_PAGE_COUNT: int = 99

# Number of records expected after fetching `Tag`s
# with a page number that exceeds the number of
# pages:
FETCH_TAG_WITH_PAGE_EXCEEDING_PAGE_COUNT_RECORD_COUNT: int = 0

# Limit number used in testing fetch tag
# with limit tests.
FETCH_TAG_WITH_LIMIT: int = 4

# Valid `Tag` id numbers in fetch with limit
# tests.
FETCH_TAG_WITH_LIMIT_VALID_IDS: List[int] = [1, 2, 5, 7]

# Limit number used in testing fetch tag
# with page and limit tests.
FETCH_TAG_WITH_PAGE_AND_LIMIT_LIMIT_NUMBER: int = 2

# Valid `Tag` id numbers in fetch with page and limit
# tests.
FETCH_TAG_WITH_PAGE_AND_LIMIT_VALID_IDS: List[int] = [1, 5]

# Id used for testing fetch by tag id
# DNE tests.
FETCH_TAG_BY_ID_DNE: int = 99999

# Valid `Tag` records dictionary.
VALID_TAG_RECORDS: dict = {
    TAG_ID_1: {
        "id": 1,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "filter::site:Melbourne",
    },
    TAG_ID_2: {
        "id": 2,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "filter::site:Rochester",
    },
    TAG_ID_3: {
        "id": 3,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "restricted::department:GeoSpatial",
    },
    TAG_ID_4: {
        "id": 4,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "restricted::department:Imaging",
    },
    TAG_ID_5: {
        "id": 5,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "Engineering Tag",
    },
    TAG_ID_6: {
        "id": 6,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "Operations Tag",
    },
    TAG_ID_7: {
        "id": 7,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "Finance Tag",
    },
    TAG_ID_8: {
        "id": 8,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "Human Resources Tag",
    },
}
