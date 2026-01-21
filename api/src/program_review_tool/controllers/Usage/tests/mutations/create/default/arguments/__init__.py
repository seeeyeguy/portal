"""
Arguments to be shared for Usage's create
controller pytests.
"""

from typing import List

# `User` email used for testing create `Usage`.
CREATE_USAGE_USER_EMAIL: str = "May.Parker@harris.com"

# `User` DNE email used for testing failure case.
CREATE_USAGE_USER_EMAIL_DNE: str = "non.existing.user@harris.com"

CREATE_USAGE_PROGRAM_PAS: List[str] = ["TEST1", "TEST2"]

CREATE_USAGE_EXPECTED_USAGE: dict = {
    "id": 2,
    "user": CREATE_USAGE_USER_EMAIL,
    "programs": CREATE_USAGE_PROGRAM_PAS,
    "duration": None,
    "success": None,
    "error_msg": None,
}
