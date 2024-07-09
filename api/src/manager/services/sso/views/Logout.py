"""
API view module for SSO service. Module provides
the `Logout` view to process a logout request from the client.
If a user is authenticated, the view will return a redirect
uri to the client that they may use to complete their logout
request.
"""

import requests

from django import http
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from manager.settings import SSO_ORIGIN
from manager.utils.types.request import DjangoHttpRequest


class Logout(APIView):
    """View to handle SSO Client logout requests."""

    permissions_classes = (IsAuthenticated,)

    def get(self, request: DjangoHttpRequest) -> http.HttpResponseRedirect:
        """Logout a user."""

        resp = requests.get(f"{SSO_ORIGIN}/oauth2/logout", verify=False, timeout=480)
        if resp.ok:
            logout(request)
            logout_url = resp.json()
            return redirect(logout_url)
        return redirect("/")
