"""
Error/Exception Module for BI Portal `Analytics` Module.
"""


class AnalyticsError(Exception):
    """Base Error for BI Portal `Analytics`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of BI Portal `Analytics` Error."""

        return f"Analytics Error (message={self.message}, status={self.status})"
