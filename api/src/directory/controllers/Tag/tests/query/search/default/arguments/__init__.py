"""
Arguments to be shared for Tag's search
controller pytests.
"""

SEARCH_TERM: str = "filter::site:"
SEARCH_TERM_NO_RESULTS: str = "no results"

# Expected `Tag` records using SEARCH_TERM.
EXPECTED_TAG_RECORDS = {
    1: {
        "id": 1,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "filter::site:Melbourne",
    },
    2: {
        "id": 2,
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
        "label": "filter::site:Rochester",
    },
}
