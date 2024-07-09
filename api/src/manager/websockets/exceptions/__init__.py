"""Error/Exception Module for WebSocket Consumers/Factories
"""


class APIConsumerFactoryConfigError(Exception):
    """Error for APIConsumerFactory.__init__."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        """Str Representation of API Consumer Factory Config Error."""

        return f"API Consumer Factory improperly configured(message={self.message})"
