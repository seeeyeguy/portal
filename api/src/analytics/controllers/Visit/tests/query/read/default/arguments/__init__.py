"""
Arguments to be shared for Visit's fetch
controller pytests.
"""

# --- Default baseline ---
# baseline record(s) created in setUp
FETCH_VISIT_RECORD_COUNT: int = 2

# --- Pagination ---
FETCH_VISIT_WITH_PAGE: int = 1
FETCH_VISIT_WITH_PAGE_RECORD_COUNT: int = 1

# --- Limit ---
FETCH_VISIT_WITH_LIMIT: int = 1
FETCH_VISIT_WITH_LIMIT_RECORD_COUNT: int = 1

# --- Page + Limit ---
FETCH_VISIT_WITH_PAGE_AND_LIMIT_RECORD_COUNT: int = 1

# --- By User ---
FETCH_VISIT_BY_USER: str = "May.Parker@harris.com"
FETCH_VISIT_BY_USER_RECORD_COUNT: int = 2  # one aggregated resource row
FETCH_VISIT_BY_USER_DNE: str = "ghost@example.com"

# --- By Resource ---
# placeholder, replaced dynamically in tests
FETCH_VISIT_BY_RESOURCE_ID: int = 1
FETCH_VISIT_BY_RESOURCE_RECORD_COUNT: int = 1
FETCH_VISIT_BY_RESOURCE_ID_DNE: int = 9999996

# --- Top ---
FETCH_VISIT_WITH_TOP: int = 1
FETCH_VISIT_WITH_TOP_RECORD_COUNT: int = 1
FETCH_VISIT_BY_USER_WITH_TOP: int = 1
FETCH_VISIT_BY_USER_WITH_TOP_RECORD_COUNT: int = 1

FETCH_VISIT_BY_USER_AND_RESOURCE_RECORD_COUNT: int = 1
FETCH_VISIT_WITH_PAGE_AND_LIMIT: int = 1
FETCH_VISIT_WITH_PAGE_AND_LIMIT_RECORD_COUNT: int = 1
