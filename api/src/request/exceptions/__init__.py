"""
Error/Exception Module for BI Portal `Request` Module.
"""


class RequestError(Exception):
    """Base Error for BI Portal `Request`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of BI Portal `Request` Error."""

        return f"Request Error (message={self.message}, status={self.status})"
