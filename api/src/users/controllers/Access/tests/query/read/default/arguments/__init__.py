"""
Arguments to be shared for Access's fetch
controller pytests.
"""

from typing import List

# All `Access` ids used to ensure the validity of our success case.
FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS: List[int] = [1, 2, 3, 4, 5, 6]

# Email related to a `User` who has an appropriate admin `Access`.
FETCH_ACCESSES_ADMIN_USER_EMAIL: str = "Tony.Stark@harris.com"

# Email for `User` related to `Access` records used in testing success case.
FETCH_ACCESSES_BY_USER_USER_EMAIL: str = "Ben.Reilly@harris.com"

# Id to fetch `Access` record used in testing success case.
FETCH_ACCESS_BY_ID_ACCESS_ID: int = 1

# Valid `Access` record ids used in testing success case.
FETCH_ACCESSES_VALID_ACCESS_RECORD_IDS: List[int] = [1, 2, 3, 4, 5]

# `Role` levels to fetch `Access` records used in testing success case.
FETCH_ACCESSES_WITH_ROLE_LEVELS_ROLE_LEVELS: List[int] = [2]

# Valid `Access` record ids used in testing success case when fetching with `Role` levels.
FETCH_ACCESSES_FOR_ROLE_LEVELS_ACCESS_RECORD_IDS: List[int] = [2, 4]

# Valid `Access` record ids used in testing success case when fetching with `User`.
FETCH_ACCESSES_FOR_USER_ACCESS_RECORD_IDS: List[int] = [4, 5]

# `Subfunction`s to fetch `Access` records used in testing success case.
FETCH_ACCESSES_WITH_SUBFUNCTIONS_SUBFUNCTIONS: List[int] = [1, 2]

# Valid `Access` record ids used in testing success case when fetching with `Subfunction`s.
FETCH_ACCESSES_FOR_SUBFUNCTIONS_ACCESS_RECORD_IDS: List[int] = [2, 3, 4]

# Email to fetch `Access` records with `User` and `Role`s.
FETCH_ACCESSES_WITH_USER_AND_ROLES_USER_EMAIL: str = "Ben.Reilly@harris.com"

# `Role` levels to fetch `Access` records related to a `User` and `Role`s used
# in testing success case.
FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ROLE_LEVELS: List[int] = [2]

# Valid `Access` record ids used in testing success case when fetching with `User`
# and `Role` levels.
FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ACCESS_RECORD_IDS: List[int] = [4]

# Email to fetch `Access` records with `User` and `Subfunction`s.
FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_USER_EMAIL: str = "Ben.Reilly@harris.com"

# `Subfunction`s to fetch `Access` records with `User` and `Subfunction`s.
FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_SUBFUNCTIONS: List[int] = [4]

# Valid `Access` record ids used in testing success case when fetching with `User`
# and `Subfunction`s.
FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS: List[int] = [5]

# Email to fetch `Access` records with `User`, `Role`s, and `Subfunction`s.
FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_USER_EMAIL: str = (
    "Ben.Reilly@harris.com"
)

# `Role` levels to fetch `Access` records related to a `User`, `Role` levels, and
# `Subfunction`s used in testing success case.
FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ROLE_LEVELS: List[int] = [3]

# `Subfunction`s to fetch `Access` records related to a `User`, `Role` levels, and
# `Subfunction`s used in testing success case.
FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_SUBFUNCTIONS: List[int] = [4]

# Valid `Access` record ids used in testing success case when fetching with `User`
# `Role` levels, and `Subfunction`s.
FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS: List[int] = [5]

# Id for an `Access` that does not exist used for testing failure case.
FETCH_ACCESS_BY_ID_ACCESS_DNE: int = 99

# Email for a `User` without appropriate admin permissions used in testing failure case.
FETCH_ACCESSES_NON_ADMIN_USER_EMAIL: str = "Ben.Reilly@harris.com"
