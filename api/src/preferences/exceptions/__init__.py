"""
Error/Exception Module for BI Portal `Preferences` Module.
"""


class PreferencesError(Exception):
    """Base Error for BI Portal `Preferences`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of BI Portal `Preferences` Error."""

        return f"Preferences Error (message={self.message}, status={self.status})"
