"""
Arguments to be shared for Resource's fetch
controller pytests.
"""

from typing import List

# Valid `Resource` ids.
RESOURCE_ID_1: int = 1
RESOURCE_ID_2: int = 2
RESOURCE_ID_3: int = 3
RESOURCE_ID_4: int = 4
RESOURCE_ID_5: int = 5

# Id used for testing fetch by `Resource` id
# tests.
FETCH_RESOURCE_BY_ID: int = 1

# Page number used in testing fetch `Resource`
# with page tests.
FETCH_RESOURCE_WITH_PAGE: int = 1

# Id used for testing fetch by `User`.
FETCH_RESOURCE_BY_USER: str = "May.Parker@harris.com"

# Page number that exceeds the number of
# pages used in testing fetch `Resource` with
# page tests.
FETCH_RESOURCE_WITH_PAGE_EXCEEDING_PAGE_COUNT: int = 99

# Expected record count when testing
# fetching all records.
FETCH_RESOURCE_RECORD_COUNT: int = 5

# Expected record count when testing
# fetching with page.
FETCH_RESOURCE_WITH_PAGE_RECORD_COUNT: int = 5

# Expected record count when testing
# fetching with limit.
FETCH_RESOURCE_WITH_LIMIT_RECORD_COUNT: int = 2

# Expected record count when testing
# fetching with page and limit.
FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_RECORD_COUNT: int = 2

# Number of records expected after fetching `Resource`s
# with a page number that exceeds the number of
# pages.
FETCH_RESOURCE_WITH_PAGE_EXCEEDING_PAGE_COUNT_RECORD_COUNT: int = 0

# Limit number used in testing fetch `Resource`
# with limit tests.
FETCH_RESOURCE_WITH_LIMIT: int = 2

# Valid `Resource` id numbers expected for fetch with limit
# tests.
FETCH_RESOURCE_WITH_LIMIT_VALID_IDS: List[int] = [1, 2]

# Limit number used in testing fetch `Resource`
# with page and limit tests.
FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_LIMIT_NUMBER: int = 2

# Valid `Resource` id numbers expected for fetch with page and limit
# tests.
FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_VALID_IDS: List[int] = [1, 2]

# Id used for testing fetch by `Resource` id
# DNE tests.
FETCH_RESOURCE_BY_ID_DNE: int = 99999

# Valid `Resource` records dictionary.
VALID_RESOURCE_RECORDS: dict = {
    RESOURCE_ID_1: {
        "id": 1,
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            },
            {
                "id": 2,
                "name": "Manager",
                "description": "Manager Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 2,
            },
        ],
        "subfunctions": [
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            }
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            }
        ],
        "description": "popstick.",
        "created": "2024-08-27T12:00:00-04:00",
        "uid": "e8b25711-d9a8-46f7-bddb-cef7436e2348",
        "revision_number": 1,
        "name": "Resource 1 Revision 1",
        "url": "example.org",
        "thumbnail": "/v1/media/resources/thumbnails/e8b25711-d9a8-46f7-bddb-cef7436e2348/1/resource_1.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "type": "Resource Type 1",
        "download": False,
        "active": True,
        "deleted": False,
        "previous_revision": None,
    },
    RESOURCE_ID_2: {
        "id": 2,
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            },
            {
                "id": 2,
                "name": "Manager",
                "description": "Manager Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 2,
            },
        ],
        "subfunctions": [
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            }
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            }
        ],
        "description": "pickle.",
        "created": "2024-08-28T12:00:00-04:00",
        "uid": "d085a72c-b564-4e12-b7c3-eb9d5bd33932",
        "revision_number": 1,
        "name": "Resource 2 Revision 1",
        "url": "example-2.org",
        "thumbnail": "/v1/media/resources/thumbnails/d085a72c-b564-4e12-b7c3-eb9d5bd33932/2/resource_2.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "type": "Resource Type 2",
        "download": False,
        "active": True,
        "deleted": False,
        "previous_revision": None,
    },
    RESOURCE_ID_3: {
        "id": 3,
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            },
            {
                "id": 2,
                "name": "Manager",
                "description": "Manager Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 2,
            },
        ],
        "subfunctions": [
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            }
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            }
        ],
        "description": "bar.",
        "created": "2024-08-27T12:00:00-04:00",
        "uid": "4c2c333e-68e9-4dca-8507-ce58cefde072",
        "revision_number": 1,
        "name": "Resource 3 Revision 1",
        "url": "example-3.org",
        "thumbnail": "/v1/media/resources/thumbnails/4c2c333e-68e9-4dca-8507-ce58cefde072/3/resource_3.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "type": "Resource Type 3",
        "download": False,
        "active": True,
        "deleted": False,
        "previous_revision": None,
    },
    RESOURCE_ID_4: {
        "id": 4,
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            },
            {
                "id": 2,
                "name": "Manager",
                "description": "Manager Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 2,
            },
        ],
        "subfunctions": [
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            }
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            }
        ],
        "description": "popstick.",
        "created": "2024-08-27T12:00:00-04:00",
        "uid": "589c788b-9a38-4150-af1f-80426dfd0b57",
        "revision_number": 1,
        "name": "Resource 4 Revision 1",
        "url": "example.org",
        "thumbnail": "/v1/media/resources/thumbnails/589c788b-9a38-4150-af1f-80426dfd0b57/1/resource_4.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "type": "Resource Type 4",
        "download": False,
        "active": True,
        "deleted": False,
        "previous_revision": None,
    },
    RESOURCE_ID_5: {
        "id": 5,
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            },
            {
                "id": 2,
                "name": "Manager",
                "description": "Manager Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 2,
            },
        ],
        "subfunctions": [
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            }
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            }
        ],
        "description": "popstick.",
        "created": "2024-08-27T12:00:00-04:00",
        "uid": "40de14f4-0983-49e9-a380-d7cfee90d696",
        "revision_number": 1,
        "name": "Resource 5 Revision 1",
        "url": "example.org",
        "thumbnail": "/v1/media/resources/thumbnails/40de14f4-0983-49e9-a380-d7cfee90d696/1/resource_5.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "type": "Resource Type 5",
        "download": False,
        "active": True,
        "deleted": False,
        "previous_revision": None,
    },
}
