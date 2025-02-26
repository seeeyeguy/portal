"""
Arguments to be used in Resource's search controller
function pytests for the `functree` structure.
"""

# pylint: disable=duplicate-code,line-too-long
from typing import List

from directory.controllers.Resource.Resource import SearchParams
from directory.controllers.Resource.search.utils import FUNCTREE_STRUCTURE


# Base parameters for search controller
# tests using `functree` structure.
BASE_SEARCH_FUNCTREE_STRUCTURE_PARAMS: SearchParams = {
    "name": "",
    "description": "",
    "functions": [],
    "subfunctions": [],
    "employee_levels": [],
    "tags": [],
    "download": None,
    "structure": FUNCTREE_STRUCTURE,  # type: ignore
    "serialize": False,
    "limit": None,
    "page": None,
}


# `Function` names.
FUNCTION_1_NAME: str = "Human Resources"
FUNCTION_2_NAME: str = "Engineering"
FUNCTION_3_NAME: str = "Finance"
FUNCTION_4_NAME: str = "Operations"

# `SubFunction` names.
FUNCTION_1_SUBFUNCTION_1_NAME: str = "Training"
FUNCTION_1_SUBFUNCTION_2_NAME: str = "Recruiting"
FUNCTION_2_SUBFUNCTION_1_NAME: str = "Software Engineering"
FUNCTION_2_SUBFUNCTION_2_NAME: str = "Mechanical Engineering"
FUNCTION_3_SUBFUNCTION_1_NAME: str = "Capital"
FUNCTION_3_SUBFUNCTION_2_NAME: str = "Cost Planning"
FUNCTION_4_SUBFUNCTION_1_NAME: str = "Quality"
FUNCTION_4_SUBFUNCTION_2_NAME: str = "General"


# Dictionary used to validate the search results
# using `functree` structure.
SEARCH_FUNCTREE_VALIDATION_MAP = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1, 3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3, 5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [3, 6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5, 7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6, 7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}


# Id's of the `Resource`s.
RESOURCE_1_REVISION_1_ID: int = 1
RESOURCE_2_REVISION_2_ID: int = 3
RESOURCE_3_REVISION_2_ID: int = 5
RESOURCE_4_REVISION_1_ID: int = 6
RESOURCE_5_REVISION_1_ID: int = 7


# Argument for search of downloadable`Resource`s.
SEARCH_DOWNLOADABLE_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3, 5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [3, 6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [6],
    },
}


# Argument for search of non-downloadable `Resource`s.
SEARCH_NON_DOWNLOADABLE_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_2_NAME: [7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1],
    },
}


# Arguments used for search by name tests.
SEARCH_BY_NAME: str = "Resource 5"
SEARCH_BY_NAME_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_2_NAME: [7],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_2_NAME: [7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [7],
    },
}


# Arguments used for search by description tests.
SEARCH_BY_DESCRIPTION: str = "orange."
SEARCH_BY_DESCRIPTION_VALIDATION_MAP: dict = {
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [3],
    },
}


# Arguments used for search by name & description tests.
SEARCH_BY_NAME_AND_DESCRIPTION_NAME_STRING: str = "Resource 3"
SEARCH_BY_NAME_AND_DESCRIPTION_DESCRIPTION_STRING: str = "watermelon."
SEARCH_BY_NAME_AND_DESCRIPTION_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [5, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_2_NAME: [5, 7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [7],
    },
}

# Arguments used for search by functions tests.
SEARCH_BY_FUNCTION_IDS: List[int] = [4, 5]
SEARCH_BY_FUNCTION_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6, 7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}


# Arguments used for search by subfunctions tests.
SEARCH_BY_SUBFUNCTION_IDS: List[int] = [1, 8]
SEARCH_BY_SUBFUNCTION_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}

# Arguments used for search by employee levels tests.
SEARCH_BY_EMPLOYEE_LEVELS_IDS: List[int] = [1, 3]
SEARCH_BY_EMPLOYEE_LEVELS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5, 7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6, 7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}

# Arguments used for search by tags tests.
SEARCH_BY_TAGS_IDS: List[int] = [1, 8]
SEARCH_BY_TAGS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5, 7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6, 7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}

# Arguments used for search by function and subfunction
# tests.
SEARCH_BY_FUNCTION_SUBFUNCTION_FUNCTION_IDS: List[int] = [3, 4]
SEARCH_BY_FUNCTION_SUBFUNCTION_SUBFUNCTION_IDS: List[int] = [5, 8]
SEARCH_BY_FUNCTION_SUBFUNCTION_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1, 3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [3, 6],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}

# Arguments used for search by functions and employee levels tests.
SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS: List[int] = [1, 2]
SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS: List[int] = [2, 3]
SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1, 3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3, 5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [3],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_2_NAME: [1],
    },
}

# Arguments used for search by functions and tags tests.
SEARCH_BY_FUNCTION_TAGS_FUNCTION_IDS: List[int] = [1, 4]
SEARCH_BY_FUNCTION_TAGS_TAG_IDS: List[int] = [2, 3]
SEARCH_BY_FUNCTION_TAGS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [6],
    },
}

# Arguments used for search by subfunctions and employee levels tests.
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS: List[int] = [1, 2]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS: List[int] = [1, 2]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_2_NAME: [7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1],
    },
}

# Arguments used for search by subfunctions and tags tests.
SEARCH_BY_SUBFUNCTION_TAGS_SUBFUNCTION_IDS: List[int] = [1, 3, 6]
SEARCH_BY_SUBFUNCTION_TAGS_TAG_IDS: List[int] = [2, 3]
SEARCH_BY_SUBFUNCTION_TAGS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3, 5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [3],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5],
    },
}

# Arguments used for search by employee levels and tags tests.
SEARCH_BY_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS: List[int] = [1, 3]
SEARCH_BY_EMPLOYEE_LEVELS_TAGS_TAG_IDS: List[int] = [3, 4]
SEARCH_BY_EMPLOYEE_LEVELS_TAGS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
        FUNCTION_3_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}

# Arguments used for search by functions, subfunctions and employee levels tests.
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS: List[int] = [1, 4]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS: List[int] = [1, 6]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS: List[int] = [1, 3]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1, 5],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1, 5, 7],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
        FUNCTION_2_SUBFUNCTION_2_NAME: [5],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_2_NAME: [5, 7],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [7],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1],
    },
}

# Arguments used for search by functions, subfunctions and employee levels tests.
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_FUNCTION_IDS: List[int] = [2, 3]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS: List[int] = [6, 7]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS: List[int] = [
    2,
    3,
]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS: List[int] = [4, 6]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_VALIDATION_MAP: dict = {
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [6],
    },
}

# Arguments used for search by subfunctions, employee levels and tags tests.
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS: List[int] = [2, 3, 5]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS: List[int] = [1, 3]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS: List[int] = [2, 4, 5]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_VALIDATION_MAP: dict = {
    FUNCTION_1_NAME: {
        FUNCTION_1_SUBFUNCTION_1_NAME: [1],
        FUNCTION_1_SUBFUNCTION_2_NAME: [1],
    },
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [1],
    },
    FUNCTION_3_NAME: {
        FUNCTION_3_SUBFUNCTION_1_NAME: [6],
    },
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [1, 6],
    },
}

# Arguments used for search with limit tests.
SEARCH_LIMIT_NUMBER: int = 2
SEARCH_LIMIT_VALIDATION_MAP: dict = {
    FUNCTION_2_NAME: {
        FUNCTION_2_SUBFUNCTION_1_NAME: [3],
        FUNCTION_2_SUBFUNCTION_2_NAME: [3],
    },
    FUNCTION_3_NAME: {FUNCTION_3_SUBFUNCTION_1_NAME: [3, 6]},
    FUNCTION_4_NAME: {
        FUNCTION_4_SUBFUNCTION_1_NAME: [6],
        FUNCTION_4_SUBFUNCTION_2_NAME: [6],
    },
}

VALID_RESOURCE_MAP: dict = {
    RESOURCE_1_REVISION_1_ID: {
        "id": 1,
        "uid": "deb17c21-e342-4a19-83ee-79a9c50f26ba",
        "previous_revision": None,
        "revision_number": 1,
        "name": "Resource 1 Revision 1",
        "description": "apple.",
        "url": "example.org",
        "thumbnail": "/v1/media/resources/thumbnails/deb17c21-e342-4a19-83ee-79a9c50f26ba/2024_08_27__16_00_00/resource_1.png",
        "primary_point_of_contact": "May.Parker@harris.com",
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
                "id": 3,
                "name": "Executive",
                "description": "Executive Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 3,
            },
        ],
        "subfunctions": [
            {
                "id": 2,
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 8,
                "name": "General",
                "description": "Function 4 SubFunction 2.",
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 3,
                "name": "Software Engineering",
                "description": "Function 2 SubFunction 1.",
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 1,
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 6,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Operations Tag",
            },
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            },
            {
                "id": 4,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:Imaging",
            },
        ],
        "type": "Resource Type 1",
        "download": False,
        "active": True,
        "created": "2024-08-27T12:00:00-04:00",
        "favorited_by": ["May.Parker@harris.com"],
        "site": ["Melbourne"],
        "restricted": {"department": ["Imaging"]},
    },
    RESOURCE_2_REVISION_2_ID: {
        "id": 3,
        "uid": "a9f5e437-88de-4e38-9a07-efb912af8108",
        "previous_revision": 2,
        "revision_number": 2,
        "name": "Resource 2 Revision 2",
        "description": "orange.",
        "url": "example-2.org",
        "thumbnail": "/v1/media/resources/thumbnails/a9f5e437-88de-4e38-9a07-efb912af8108/2024_08_28__16_00_00/resource_2.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "employee_levels": [
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
                "id": 4,
                "name": "Mechanical Engineering",
                "description": "Function 2 SubFunction 2.",
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 5,
                "name": "Capital",
                "description": "Function 3 SubFunction 1.",
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 3,
                "name": "Software Engineering",
                "description": "Function 2 SubFunction 1.",
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 5,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Engineering Tag",
            },
            {
                "id": 2,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Rochester",
            },
            {
                "id": 4,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:Imaging",
            },
        ],
        "type": "Resource Type 2",
        "download": True,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
        "favorited_by": ["Peter.Parker@harris.com", "May.Parker@harris.com"],
        "site": ["Rochester"],
        "restricted": {"department": ["Imaging"]},
    },
    RESOURCE_3_REVISION_2_ID: {
        "id": 5,
        "uid": "ed473d39-6fa7-4e36-8ae1-1d1de940563a",
        "previous_revision": 4,
        "revision_number": 2,
        "name": "Resource 3 Revision 2",
        "description": "banana.",
        "url": "example-3.org",
        "thumbnail": "/v1/media/resources/thumbnails/ed473d39-6fa7-4e36-8ae1-1d1de940563a/2024_08_28__16_00_00/resource_3.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "employee_levels": [
            {
                "id": 3,
                "name": "Executive",
                "description": "Executive Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 3,
            },
        ],
        "subfunctions": [
            {
                "id": 6,
                "name": "Cost Planning",
                "description": "Function 3 SubFunction 2.",
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 2,
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 4,
                "name": "Mechanical Engineering",
                "description": "Function 2 SubFunction 2.",
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 1,
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            },
            {
                "id": 7,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Finance Tag",
            },
            {
                "id": 3,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:GeoSpatial",
            },
        ],
        "type": "Resource Type 3",
        "download": True,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
        "favorited_by": ["Tony.Stark@harris.com", "Peter.Parker@harris.com"],
        "site": ["Melbourne"],
        "restricted": {"department": ["GeoSpatial"]},
    },
    RESOURCE_4_REVISION_1_ID: {
        "id": 6,
        "uid": "367d5c78-10b8-4464-9190-e9705ae4997b",
        "previous_revision": None,
        "revision_number": 1,
        "name": "Resource 4 Revision 1",
        "description": "grape.",
        "url": "example-4.org",
        "thumbnail": "/v1/media/resources/thumbnails/367d5c78-10b8-4464-9190-e9705ae4997b/2024_08_28__16_00_00/resource_4.png",
        "primary_point_of_contact": "May.Parker@harris.com",
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
                "id": 7,
                "name": "Quality",
                "description": "Function 4 SubFunction 1.",
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 8,
                "name": "General",
                "description": "Function 4 SubFunction 2.",
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 5,
                "name": "Capital",
                "description": "Function 3 SubFunction 1.",
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 5,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Engineering Tag",
            },
            {
                "id": 2,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Rochester",
            },
            {
                "id": 8,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Human Resources Tag",
            },
            {
                "id": 4,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:Imaging",
            },
        ],
        "type": "Resource Type 4",
        "download": True,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
        "favorited_by": ["Tony.Stark@harris.com", "May.Parker@harris.com"],
        "site": ["Rochester"],
        "restricted": {"department": ["Imaging"]},
    },
    RESOURCE_5_REVISION_1_ID: {
        "id": 7,
        "uid": "caebfad3-1cc2-40db-a8cf-70e56f289d98",
        "previous_revision": None,
        "revision_number": 1,
        "name": "Resource 5 Revision 1",
        "description": "watermelon.",
        "url": "example-4.org",
        "thumbnail": "/v1/media/resources/thumbnails/caebfad3-1cc2-40db-a8cf-70e56f289d98/2024_08_28__16_00_00/resource_5.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            },
        ],
        "subfunctions": [
            {
                "id": 6,
                "name": "Cost Planning",
                "description": "Function 3 SubFunction 2.",
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 7,
                "name": "Quality",
                "description": "Function 4 SubFunction 1.",
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 2,
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 6,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Operations Tag",
            },
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            },
            {
                "id": 7,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Finance Tag",
            },
        ],
        "type": "Resource Type 5",
        "download": False,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
        "favorited_by": ["Tony.Stark@harris.com"],
        "site": ["Melbourne"],
        "restricted": {},
    },
}
