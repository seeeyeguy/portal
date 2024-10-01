"""
Arguments to be shared for Resource's search
controller pytests for both `default` and `functree`
structures.
"""

from typing import List


# A name that does not exist for any `Resource`.
SEARCH_BY_NAME_DNE: str = "DNE_NAME"

# A description that does not exist for any `Resource`.
SEARCH_BY_DESCRIPTION_DNE: str = "DNE_DESCRIPTION"

# `Function` id that does not exist in a list.
SEARCH_BY_FUNCTIONS_DNE: List[int] = [1111]

# `SubFunction` id that does not exist in a list.
SEARCH_BY_SUBFUNCTIONS_DNE: List[int] = [2222]

# `EmployeeLevel` id that does not exist in a list.
SEARCH_BY_EMPLOYEE_LEVELS_DNE: List[int] = [3333]

# `Tag` id that does not exist in a list.
SEARCH_BY_TAGS_DNE: List[int] = [2222]

# A number that exceeds the number of pages
# in a search.
SEARCH_EXCEEDING_PAGE_NUMBER: int = 99999
