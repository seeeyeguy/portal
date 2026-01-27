"""
Arguments to be shared for Content's fetch
controller pytests.
"""

FETCH_CONTENT_CONTENT_KEY: str = "test/key"
FETCH_CONTENT_CONTENT_CONTENT: dict = {"data": "content"}

FETCH_CONTENT_CONTENT_KEY_DNE: str = "test/key/dne"

EXPECTED_CONTENT_RECORD: dict = {
    "id": 1,
    "created": "2024-08-27T12:00:00-04:00",
    "modified": "2024-08-27T12:00:00-04:00",
    "key": "test/key",
    "content": {"data": "content"},
    "modified_by": "May.Parker@harris.com",
}
