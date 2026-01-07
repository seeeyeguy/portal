"""
Arguments to be shared for Usage's fetch controller pytests.
"""

from typing import List

FETCH_USAGE_USER = "May.Parker@harris.com"
FETCH_USAGE_RECORD_COUNT = 1

FETCH_USAGE_EXPECTED_RECORDS = {
    1: {
        "id": 1,
        "user": "May.Parker@harris.com",
        "duration": None,
        "success": True,
        "error_msg": "",
        "programs": ["6C27", "10LR"],
    }
}


FETCH_USAGE_ERROR_TOP = "Top must be a positive integer"
FETCH_USAGE_ERROR_INVALID_USER = "User (username=invalid@example.com) does not exist."
INVALID_USER = "invalid@example.com"
FETCH_USAGE_PAGE = 1
FETCH_USAGE_LIMIT = 1
INVALID_USAGE_PAGE = -1
INVALID_USAGE_LIMIT = -5


FETCH_USAGE_PA_NUMBER = "6C27"
FETCH_USAGE_INVALID_PA_NUMBER = "NON_EXISTENT_PA"
FETCH_USAGE_SUCCESS_TRUE = True
FETCH_USAGE_SUCCESS_FALSE = False
