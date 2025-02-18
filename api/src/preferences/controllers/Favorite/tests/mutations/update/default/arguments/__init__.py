"""
Arguments to be shared for Favorite's rank
controller pytests.
"""

from typing import List

# `User` email used for testing ranking `Favorite`(s).
RANK_FAVORITE_USER_EMAIL: str = "Tony.Stark@harris.com"

# `Favorite` ids used for testing rank `Favorite`(s).
RANK_FAVORITE_FAVORITE_ID_1: int = 1
RANK_FAVORITE_FAVORITE_ID_2: int = 2

# `User` DNE email used for testing failure case.
RANK_FAVORITE_USER_EMAIL_DNE: str = "DNE.User@harris.com"

# `Favorite` DNE id used for testing failure case.
RANK_FAVORITE_FAVORITE_ID_DNE: int = 9999

# Ranks used for test ranking `Favorite`(s).
RANK_FAVORITE_FAVORITE_1_RANK: int = 2
RANK_FAVORITE_FAVORITE_2_RANK: int = 1

# Ranks used for testing a rank mismatch in
# ranking `Favorite`(s).
RANK_FAVORITE_FAVORITE_1_MISMATCH_RANK: int = 3
RANK_FAVORITE_FAVORITE_2_MISMATCH_RANK: int = 4

# Ranked favorites param used for testing ranking `Favorite`(s).
RANK_FAVORITE_RANKED_FAVORITES_PARAM: List[dict] = [
    {"id": RANK_FAVORITE_FAVORITE_ID_1, "rank": RANK_FAVORITE_FAVORITE_1_RANK},
    {"id": RANK_FAVORITE_FAVORITE_ID_2, "rank": RANK_FAVORITE_FAVORITE_2_RANK},
]

# Ranked favorites param used for testing ranking `Favorite`(s) where
# the `Favorite` does not exist.
RANK_FAVORITE_RANKED_FAVORITES_PARAM_FAVORITE_DNE: List[dict] = [
    {"id": RANK_FAVORITE_FAVORITE_ID_DNE, "rank": RANK_FAVORITE_FAVORITE_1_RANK},
    {"id": RANK_FAVORITE_FAVORITE_ID_2, "rank": RANK_FAVORITE_FAVORITE_2_RANK},
]

# Ranked favorites param used for testing ranking `Favorite`(s) where
# there's a mismatch in between the existing ranks and the ones supplied
# for the update.
RANK_FAVORITE_RANKED_FAVORITES_PARAM_MISMATCH_RANKS: List[dict] = [
    {
        "id": RANK_FAVORITE_FAVORITE_ID_1,
        "rank": RANK_FAVORITE_FAVORITE_1_MISMATCH_RANK,
    },
    {
        "id": RANK_FAVORITE_FAVORITE_ID_2,
        "rank": RANK_FAVORITE_FAVORITE_2_MISMATCH_RANK,
    },
]

# Ranked favorites param used for testing ranking `Favorite`(s) where
# there's duplicate
RANK_FAVORITE_RANKED_FAVORITES_PARAM_DUPLICATE_RANK: List[dict] = [
    {"id": RANK_FAVORITE_FAVORITE_ID_1, "rank": RANK_FAVORITE_FAVORITE_1_RANK},
    {"id": RANK_FAVORITE_FAVORITE_ID_2, "rank": RANK_FAVORITE_FAVORITE_1_RANK},
]

VALID_RANKED_FAVORITES: List[dict] = [
    {
        "id": 1,
        "user": {
            "id": 3,
            "username": "Tony.Stark@harris.com",
            "email": "Tony.Stark@harris.com",
            "first_name": "Tony",
            "last_name": "Stark",
            "is_active": True,
        },
        "resource": {
            "id": 1,
            "employee_levels": [
                {
                    "id": 1,
                    "name": "Employee",
                    "description": "Employee Level 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                    "level": 1,
                }
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
            "description": "Test Resource 1.",
            "created": "2025-01-01T11:00:00-05:00",
            "uid": "5b2c3458-e21f-4621-bbfb-06d5a7015943",
            "revision_number": 1,
            "name": "Resource 1 Revision 1",
            "url": "example-resource-1.org",
            "thumbnail": "/v1/media/resources/thumbnails/5b2c3458-e21f-4621-bbfb-06d5a7015943/1/resource_1.png",
            "primary_point_of_contact": "May.Parker@harris.com",
            "type": "Resource Type 1",
            "download": False,
            "active": True,
            "previous_revision": None,
        },
        "rank": 2,
        "created": "2025-01-02T11:00:00-05:00",
    },
    {
        "id": 2,
        "user": {
            "id": 3,
            "username": "Tony.Stark@harris.com",
            "email": "Tony.Stark@harris.com",
            "first_name": "Tony",
            "last_name": "Stark",
            "is_active": True,
        },
        "resource": {
            "id": 2,
            "employee_levels": [
                {
                    "id": 3,
                    "name": "Executive",
                    "description": "Executive Level 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                    "level": 3,
                }
            ],
            "subfunctions": [
                {
                    "id": 4,
                    "function": {
                        "id": 2,
                        "name": "Engineering",
                        "description": "Function 2.",
                        "created": "2024-08-27T12:00:00-04:00",
                        "modified": "2024-08-27T12:00:00-04:00",
                    },
                    "name": "Mechanical Engineering",
                    "description": "Function 2 SubFunction 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                }
            ],
            "tags": [
                {
                    "id": 2,
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                    "label": "filter::site:Rochester",
                }
            ],
            "description": "Test Resource 2.",
            "created": "2025-01-01T11:00:00-05:00",
            "uid": "700e78ea-f14a-437a-801a-f5b3ffa800fd",
            "revision_number": 1,
            "name": "Resource 2 Revision 1",
            "url": "example-resource-2.org",
            "thumbnail": "/v1/media/resources/thumbnails/700e78ea-f14a-437a-801a-f5b3ffa800fd/2/resource_2.png",
            "primary_point_of_contact": "May.Parker@harris.com",
            "type": "Resource Type 2",
            "download": False,
            "active": True,
            "previous_revision": None,
        },
        "rank": 1,
        "created": "2024-01-02T11:00:00-05:00",
    },
]
