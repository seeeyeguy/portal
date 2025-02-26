"""
Arguments to be used in Resource's search controller
function pytests for the `default` structure.
"""

# pylint: disable=duplicate-code,line-too-long
from typing import List, Literal, Tuple

from directory.controllers.Resource.Resource import SearchParams
from directory.controllers.Resource.search.utils import DEFAULT_STRUCTURE


# Base parameters for search controller
# tests using `default` structure.
BASE_SEARCH_DEFAULT_STRUCTURE_PARAMS: SearchParams = {
    "name": "",
    "description": "",
    "functions": [],
    "subfunctions": [],
    "employee_levels": [],
    "tags": [],
    "download": None,
    "structure": DEFAULT_STRUCTURE,  # type: ignore
    "serialize": False,
    "limit": None,
    "page": None,
}


# Id's of the `Resource`s.
RESOURCE_1_REVISION_2_ID: int = 2
RESOURCE_2_REVISION_2_ID: int = 4
RESOURCE_3_REVISION_1_ID: int = 5
RESOURCE_4_REVISION_1_ID: int = 6
RESOURCE_5_REVISION_1_ID: int = 7

# List of all valid `Resource` ids.
VALID_RESOURCE_IDS: List[int] = [
    RESOURCE_1_REVISION_2_ID,
    RESOURCE_2_REVISION_2_ID,
    RESOURCE_3_REVISION_1_ID,
    RESOURCE_4_REVISION_1_ID,
    RESOURCE_5_REVISION_1_ID,
]

# Argument for search of downloadable`Resource`s.
SEARCH_DOWNLOADABLE_RESOURCE_IDS: List[int] = [5, 7]

# Argument for search of non-downloadable `Resource`s.
SEARCH_NON_DOWNLOADABLE_RESOURCE_IDS: List[int] = [2, 4, 6]

# Arguments used for search by name tests.
SEARCH_BY_NAME: str = "Resource 2 Revision 2"
SEARCH_BY_NAME_RESOURCE_IDS: List[int] = [4]

# Arguments used for search by description tests.
SEARCH_BY_DESCRIPTION: str = "popstick."
SEARCH_BY_DESCRIPTION_RESOURCE_IDS: List[int] = [2]

# Arguments used for search by name & description tests.
SEARCH_BY_NAME_AND_DESCRIPTION_NAME_STRING: str = "Resource 1"
SEARCH_BY_NAME_AND_DESCRIPTION_DESCRIPTION_STRING: str = "ice cream."
SEARCH_BY_NAME_AND_DESCRIPTION_RESOURCE_IDS: List[int] = [2, 7]

# Arguments used for search by functions tests.
SEARCH_BY_FUNCTION_IDS: List[int] = [1, 2]
SEARCH_BY_FUNCTION_RESOURCE_IDS: List[int] = [2, 4, 7]

# Arguments used for search by subfunctions tests.
SEARCH_BY_SUBFUNCTION_IDS: List[int] = [5, 7]
SEARCH_BY_SUBFUNCTION_RESOURCE_IDS: List[int] = [5, 6]

# Arguments used for search by employee levels tests.
SEARCH_BY_EMPLOYEE_LEVELS_IDS: List[int] = [1, 2]
SEARCH_BY_EMPLOYEE_LEVELS_RESOURCE_IDS: List[int] = [2, 4, 6, 7]

# Arguments used for search by tags tests.
SEARCH_BY_TAGS_IDS: List[int] = [3, 4]
SEARCH_BY_TAGS_RESOURCE_IDS: List[int] = [5, 6]

# Arguments used for search by function and subfunction
# tests.
SEARCH_BY_FUNCTION_SUBFUNCTION_FUNCTION_IDS: List[int] = [1, 2]
SEARCH_BY_FUNCTION_SUBFUNCTION_SUBFUNCTION_IDS: List[int] = [1, 2, 3, 4]
SEARCH_BY_FUNCTION_SUBFUNCTION_RESOURCE_IDS: List[int] = [2, 4, 7]

# Arguments used for search by functions and employee levels tests.
SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS: List[int] = [3, 4]
SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS: List[int] = [1, 3]
SEARCH_BY_FUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS: List[int] = [5, 7]

# Arguments used for search by functions and tags tests.
SEARCH_BY_FUNCTION_TAGS_FUNCTION_IDS: List[int] = [1, 4]
SEARCH_BY_FUNCTION_TAGS_TAG_IDS: List[int] = [1, 7]
SEARCH_BY_FUNCTION_TAGS_RESOURCE_IDS: List[int] = [2, 4, 6, 7]

# Arguments used for search by subfunctions and employee levels tests.
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS: List[int] = [3, 5]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS: List[int] = [1, 2]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS: List[int] = [7]

# Arguments used for search by subfunctions and tags tests.
SEARCH_BY_SUBFUNCTION_TAGS_SUBFUNCTION_IDS: List[int] = [2, 5, 8]
SEARCH_BY_SUBFUNCTION_TAGS_TAG_IDS: List[int] = [1, 8]
SEARCH_BY_SUBFUNCTION_TAGS_RESOURCE_IDS: List[int] = [4, 7]

# Arguments used for search by employee levels and tags tests.
SEARCH_BY_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS: List[int] = [2, 3]
SEARCH_BY_EMPLOYEE_LEVELS_TAGS_TAG_IDS: List[int] = [2, 4]
SEARCH_BY_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS: List[int] = [4, 6]

# Arguments used for search by functions, subfunctions and employee levels tests.
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_FUNCTION_IDS: List[int] = [2, 4]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_SUBFUNCTION_IDS: List[int] = [5, 8]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_EMPLOYEELEVEL_IDS: List[int] = [1, 2]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_RESOURCE_IDS: List[int] = [6, 7]

# Arguments used for search by functions, subfunctions and employee levels tests.
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_FUNCTION_IDS: List[int] = [1, 3]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS: List[int] = [1, 5]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS: List[int] = [
    1,
    3,
]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS: List[int] = [1, 2, 6]
SEARCH_BY_FUNCTION_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS: List[int] = [2, 4, 5]

# Arguments used for search by subfunctions, employee levels and tags tests.
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_SUBFUNCTION_IDS: List[int] = [2, 5, 8]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_EMPLOYEELEVEL_IDS: List[int] = [3, 5]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_TAG_IDS: List[int] = [1, 6, 8]
SEARCH_BY_SUBFUNCTION_EMPLOYEE_LEVELS_TAGS_RESOURCE_IDS: List[int] = [4, 5]


# Arguments used for search with limit tests.
SEARCH_LIMIT_NUMBER: int = 3
SEARCH_LIMIT_RESOURCE_IDS: List[int] = [4, 5, 6]


VALID_RESOURCE_MAP: dict = {
    RESOURCE_1_REVISION_2_ID: {
        "id": 2,
        "uid": "e8b25711-d9a8-46f7-bddb-cef7436e2348",
        "previous_revision": 1,
        "revision_number": 2,
        "name": "Resource 1 Revision 2",
        "description": "popstick.",
        "url": "example.org",
        "thumbnail": "/v1/media/resources/thumbnails/e8b25711-d9a8-46f7-bddb-cef7436e2348/2024_08_28__16_00_00/resource_1.png",
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
        "type": "Resource Type 1",
        "download": False,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
    },
    RESOURCE_2_REVISION_2_ID: {
        "id": 4,
        "uid": "4c2c333e-68e9-4dca-8507-ce58cefde072",
        "previous_revision": 3,
        "revision_number": 2,
        "name": "Resource 2 Revision 2",
        "description": "bar.",
        "url": "example-2.org",
        "thumbnail": "/v1/media/resources/thumbnails/4c2c333e-68e9-4dca-8507-ce58cefde072/2024_08_28__16_00_00/resource_2.png",
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
                "id": 2,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Rochester",
            },
        ],
        "type": "Resource Type 2",
        "download": False,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
    },
    RESOURCE_3_REVISION_1_ID: {
        "id": 5,
        "uid": "a157e2a8-1db7-4ef2-adc1-90e109af0557",
        "previous_revision": None,
        "revision_number": 1,
        "name": "Resource 3 Revision 1",
        "description": "cake.",
        "url": "example-3.org",
        "thumbnail": "/v1/media/resources/thumbnails/a157e2a8-1db7-4ef2-adc1-90e109af0557/2024_08_28__16_00_00/resource_3.png",
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
                "id": 6,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Operations Tag",
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
    },
    RESOURCE_4_REVISION_1_ID: {
        "id": 6,
        "uid": "0e8ec5b9-11b5-44b6-9b16-6a4d69067d46",
        "previous_revision": None,
        "revision_number": 1,
        "name": "Resource 4 Revision 1",
        "description": "cookie.",
        "url": "example-4.org",
        "thumbnail": "/v1/media/resources/thumbnails/0e8ec5b9-11b5-44b6-9b16-6a4d69067d46/2024_08_28__16_00_00/resource_4.png",
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
        ],
        "tags": [
            {
                "id": 7,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Finance Tag",
            },
            {
                "id": 4,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:Imaging",
            },
            {
                "id": 3,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:GeoSpatial",
            },
        ],
        "type": "Resource Type 4",
        "download": False,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
    },
    RESOURCE_5_REVISION_1_ID: {
        "id": 7,
        "uid": "b7801c65-640e-403e-8f67-0a6b219f01ac",
        "previous_revision": None,
        "revision_number": 1,
        "name": "Resource 5 Revision 1",
        "description": "ice cream.",
        "url": "example-4.org",
        "thumbnail": "/v1/media/resources/thumbnails/b7801c65-640e-403e-8f67-0a6b219f01ac/2024_08_28__16_00_00/resource_5.png",
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
        ],
        "tags": [
            {
                "id": 8,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "Human Resources Tag",
            },
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            },
            {
                "id": 2,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Rochester",
            },
        ],
        "type": "Resource Type 5",
        "download": True,
        "active": True,
        "created": "2024-08-28T12:00:00-04:00",
    },
}
