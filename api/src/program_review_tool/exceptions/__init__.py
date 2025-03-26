"""
Error/Exception Module for `ProgramReviewTool` Module.
"""


class ProgramReviewToolError(Exception):
    """Base Error for `ProgramReviewTool`."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """String Representation of `ProgramReviewTool` Error."""

        return f"ProgramReviewTool Error (message={self.message}, status={self.status})"
