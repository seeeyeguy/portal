"""Error/Exception Module for Application Services
"""

from manager.settings import ApplicationServices


class ServicesError(Exception):
    """Base Error for Service Provider."""

    def __init__(self, service: str, message: str, status: int, *args: object) -> None:
        super().__init__(*args)
        self.service = service
        self.message = message
        self.status = status

    def __str__(self) -> str:
        """Str Representation of Services Error."""

        return (
            f"Service Error(service={self.service}, "
            f"message={self.message}, status={self.status})"
        )


class LDAPServiceError(ServicesError):
    """Error for LDAP Service Provider."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(ApplicationServices.LDAP, message, status, *args)


class SSOServiceError(ServicesError):
    """Error for SSO Service Provider."""

    def __init__(self, message: str, status: int, *args: object) -> None:
        super().__init__(ApplicationServices.SSO, message, status, *args)
