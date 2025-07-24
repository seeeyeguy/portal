"""
Arguments to be shared for Usage's complete
controller pytests.
"""

from typing import List

# `Usage` ID used for testing complete `Usage`.
COMPLETE_USAGE_ID: int = 2

# `Usage` ID used for testing already completed `Usage`.
COMPLETE_USAGE_ID_ALREADY_COMPLETED: int = 1

# `Usage` DNE ID used for testing failure case.
COMPLETE_USAGE_ID_DNE: int = 99

COMPLETE_USAGE_PROGRAM_PAS: List[str] = ["TEST1", "TEST2"]

COMPLETE_USAGE_FINISH_TIME = "2025-01-01T11:01:00Z"

COMPLETE_USAGE_EXPECTED_USAGE: dict = {
    "id": 2,
    "created": "2025-01-01T06:00:00-05:00",
    "user": "May.Parker@harris.com",
    "programs": COMPLETE_USAGE_PROGRAM_PAS,
    "duration": "00:01:00",
    "success": True,
    "error_msg": None,
}

COMPLETE_USAGE_ALREADY_COMPLETED_EXPECTED_USAGE: dict = {
    "id": 1,
    "created": "2025-01-01T06:00:00-05:00",
    "user": "May.Parker@harris.com",
    "programs": COMPLETE_USAGE_PROGRAM_PAS,
    "duration": "00:00:37.399048",
    "success": False,
    "error_msg": "This broke.",
}
