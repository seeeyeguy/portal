"""
Arguments to be shared for Query's fetch
controller pytests.
"""

# Valid `Query` ids.
QUERY_ID_1: int = 1
QUERY_ID_2: int = 2
QUERY_ID_3: int = 3

# Id used for testing fetch by query id
# tests.
FETCH_QUERY_BY_ID: int = 1

# Page number used for testing fetch by page.
FETCH_QUERY_WITH_PAGE: int = 1

# Id used for testing fetch by limit.
FETCH_QUERY_WITH_LIMIT: int = 2

# Id used for testing fetch by user.
FETCH_QUERY_BY_USER: str = "May.Parker@harris.com"

# Id used for testing fetch by query id
# DNE tests.
FETCH_QUERY_BY_ID_DNE: int = 999

# Id used for testing fetch by user
# DNE tests.
FETCH_QUERY_BY_USER_DNE: str = "ay.Parker@harris.com"

# Expected record count when testing
# fetching all records.
FETCH_QUERY_RECORD_COUNT: int = 3

# Expected record count when testing
# fetching with page.
FETCH_QUERY_WITH_PAGE_RECORD_COUNT: int = 3

# Expected record count when testing
# fetching with limit.
FETCH_QUERY_WITH_LIMIT_RECORD_COUNT: int = 2

# Expected record count when testing
# fetching with page and limit.
FETCH_QUERY_WITH_PAGE_AND_LIMIT_RECORD_COUNT: int = 2

# Expected record count when testing
# fetching by user with page.
FETCH_QUERY_BY_USER_WITH_PAGE_RECORD_COUNT: int = 1

# Expected record count when testing
# fetching by user with limit.
FETCH_QUERY_BY_USER_WITH_LIMIT_RECORD_COUNT: int = 1

# Expected record count when testing
# fetching by user.
FETCH_QUERY_BY_USER_RECORD_COUNT: int = 1

# Expected record count when testing
# fetching by user with page and limit.
FETCH_QUERY_BY_USER_WITH_PAGE_AND_LIMIT_RECORD_COUNT: int = 1

# Valid `Query` records dictionary.
VALID_QUERY_RECORDS: dict = {
    QUERY_ID_1: {
        "id": 1,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@harris.com",
            "first_name": "May",
            "last_name": "Parker",
            "is_active": True,
        },
        "resources": [
            {
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
                "thumbnail": "/v1/media/resources/thumbnails/e8b25711-d9a8-46f7-bddb-cef7436e2348/2024_08_27__16_00_00/resource_1.png",
                "primary_point_of_contact": "May.Parker@harris.com",
                "type": "Resource Type 1",
                "download": False,
                "active": True,
                "previous_revision": None,
            }
        ],
        "created": "2025-01-27T11:00:00-05:00",
        "search_term": "Example Search Term 1.",
    },
    QUERY_ID_2: {
        "id": 2,
        "user": {
            "id": 2,
            "username": "Peter.Parker@harris.com",
            "email": "Peter.Parker@harris.com",
            "first_name": "Peter",
            "last_name": "Parker",
            "is_active": True,
        },
        "resources": [
            {
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
                "thumbnail": "/v1/media/resources/thumbnails/d085a72c-b564-4e12-b7c3-eb9d5bd33932/2024_08_28__16_00_00/resource_2.png",
                "primary_point_of_contact": "May.Parker@harris.com",
                "type": "Resource Type 2",
                "download": False,
                "active": True,
                "previous_revision": None,
            }
        ],
        "created": "2025-01-27T11:00:00-05:00",
        "search_term": "Example Search Term 2.",
    },
    QUERY_ID_3: {
        "id": 3,
        "user": {
            "id": 3,
            "username": "Tony.Stark@harris.com",
            "email": "Tony.Stark@harris.com",
            "first_name": "Tony",
            "last_name": "Stark",
            "is_active": True,
        },
        "resources": [
            {
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
                "thumbnail": "/v1/media/resources/thumbnails/4c2c333e-68e9-4dca-8507-ce58cefde072/2024_08_27__16_00_00/resource_3.png",
                "primary_point_of_contact": "May.Parker@harris.com",
                "type": "Resource Type 3",
                "download": False,
                "active": True,
                "previous_revision": None,
            }
        ],
        "created": "2025-01-27T11:00:00-05:00",
        "search_term": "Example Search Term 3.",
    },
}
