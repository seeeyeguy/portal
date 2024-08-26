"""
Error/Exception Module for BI Portal `Directory` Module.
"""


class DirectoryError(Exception):
    """Base Error for BI Portal `Directory`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of BI Portal `Directory` Error."""

        return f"Directory Error (message={self.message}, status={self.status})"
