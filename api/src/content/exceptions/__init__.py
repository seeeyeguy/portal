"""
Error/Exception Module for `Content` Module.
"""


class ContentError(Exception):
    """Base Error for `Content`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of `Content` Error."""

        return f"Content Error (message={self.message}, status={self.status})"
