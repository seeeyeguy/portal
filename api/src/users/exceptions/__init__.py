"""
Error/Exception Module for BI Portal `Users` Module.
"""


class UsersError(Exception):
    """Base Error for BI Portal `Users`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of BI Portal `Users` Error."""

        return f"Users Error (message={self.message}, status={self.status})"
