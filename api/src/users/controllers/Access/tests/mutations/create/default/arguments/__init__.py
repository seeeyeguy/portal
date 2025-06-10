"""
Arguments to be shared for Access's create
controller pytests.
"""

from typing import List

CREATE_ACCESS_ADMIN_USER_EMAIL: str = "Tony.Stark@harris.com"

CREATE_ACCESS_NON_ADMIN_USER_EMAIL: str = "Peter.Parker@harris.com"

CREATE_ACCESS_USER_EMAIL: str = "Ben.Parker@harris.com"
CREATE_ACCESS_ROLE_LEVEL: int = 2
CREATE_ACCESS_SUBFUNCTION_IDS: List[int] = [3, 4]
CREATE_ACCESS_STAGE_LEVELS: List[int] = [2]

CREATE_ACCESS_ALREADY_EXISTS_USER_EMAIL: str = "May.Parker@harris.com"
CREATE_ACCESS_ALREADY_EXISTS_ROLE_LEVEL: int = 3
CREATE_ACCESS_ALREADY_EXISTS_SUBFUNCTION_IDS: List[int] = [1, 4]

CREATE_ACCESS_USER_EMAIL_DNE: str = "DNE.User@harris.com"

CREATE_ACCESS_ROLE_LEVEL_DNE: int = 99

CREATE_ACCESS_SUBFUNCTION_IDS_DNE: List[int] = [888, 999]

CREATE_ACCESS_STAGE_LEVELS_DNE: List[int] = [500, 700]

CREATE_ACCESS_ROLE_NOT_PERMITTED_SUBFUNCTIONS_ROLE_LEVEL: int = 1
CREATE_ACCESS_ROLE_NOT_PERMITTED_STAGES_ROLE_LEVEL: int = 3

CREATE_ACCESS_TERMINAL_STAGES_NOT_PERMITTED_STAGE_LEVELS: List[int] = [100]

CREATE_ACCESS_DRAFT_STAGE_NOT_PERMITTED_STAGE_LEVELS: List[int] = [1]

CREATE_ACCESS_INVALID_STAGES_FOR_ROLE_STAGE_LEVELS: List[int] = [3]

CREATE_ACCESS_EXPECTED_ACCESS: dict = {
    "id": 4,
    "user": {
        "id": 4,
        "username": "Ben.Parker@harris.com",
        "email": "Ben.Parker@harris.com",
        "first_name": "Ben",
        "last_name": "Parker",
        "is_active": True,
    },
    "role": {
        "id": 2,
        "created": "2024-08-27T12:00:00-04:00",
        "name": "Business Process Expert",
        "description": "Business Process Expert.",
        "level": 2,
    },
    "access_revoked_date": None,
    "stage": [
        {
            "id": 2,
            "name": "Submitted",
            "description": "A resource was submitted.",
            "level": 2,
        },
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
        },
        {
            "id": 3,
            "function": {
                "id": 2,
                "name": "Engineering",
                "description": "Function 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            "name": "Software Engineering",
            "description": "Function 2 SubFunction 1.",
            "created": "2024-08-27T12:00:00-04:00",
            "modified": "2024-08-27T12:00:00-04:00",
        },
    ],
}
