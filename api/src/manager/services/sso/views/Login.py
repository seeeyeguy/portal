""" 
API view module for SSO service. Module provides
the `Login` view to process a login request from the client.
The view awaits an encrypted authentication package from the SSO
service, consisting of the user's email and sessionkey. The
authentication package is decrypted and used to verfiy that the
user has access to the system. If so, we remove the old session
instantiated by the service and login the user, creating a new
session. Encryption and instantiating a new session provide a
more secure authentication process as now only the application
has the appropriate session key for the user.
"""

import json
import logging
from typing import Union
from cryptography.fernet import Fernet
from typing_extensions import TypedDict

from django import http
from django.contrib.auth import get_user_model, login
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from manager.settings import SSO_SERVICE_ENCRYPTION_KEY
from users.models import Profile


LOGGER = logging.getLogger(__name__)


class User(TypedDict):
    """Type annotation for User data."""

    email: str


class Package(TypedDict):
    """Type annotation for SSO auth data."""

    sessionkey: str
    user: User


class Login(APIView):
    """View to handle SSO client login requests."""

    permission_classes = (AllowAny,)

    def get(
        self, request: http.HttpRequest, auth: str
    ) -> Union[http.HttpResponseRedirect, Response]:
        """Authenticate/login a user."""

        try:
            decrypted_package = (
                Fernet(SSO_SERVICE_ENCRYPTION_KEY).decrypt(auth.encode()).decode()
            )
            package: Package = json.loads(decrypted_package)
            user = get_user_model().objects.filter(username=package["user"]["email"])
            session = Session.objects.filter(session_key=package["sessionkey"])
            if user.exists() and (
                user.first().is_authenticated  # type: ignore[union-attr]
                and session.exists()
            ):
                session.delete()
                # if the user model is extended with a Profile model.
                profile = Profile.objects.filter(user=user.first())
                if not profile.exists():
                    Profile.objects.create(user=user.first())  # type: ignore[misc]
                login(request=request, user=user.first())
                return redirect("/")
        # pylint: disable=broad-exception-caught
        except Exception as exc:
            LOGGER.error(f"SSO Login Failed: {exc}")
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_403_FORBIDDEN)
