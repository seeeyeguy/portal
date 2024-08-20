"""
API view module for LDAP requests. Proxy the LDAP service
with `search_term`, `limit`, & `offset` and return
matching entries to the client. 
"""

import json
import logging

from django import http
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework import status

from manager.services.ldap import provider
from manager.services.ldap.views import serializers
from manager.services.exceptions import LDAPServiceError
from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class LDAPSearch(View):
    """LDAP Search RESTful endpoints."""

    @method_decorator(
        with_serializer(serializer_class=serializers.LDAPSearchRequestSerializer)
    )
    def post(self, _: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/svc/ldap."""

        try:
            LOGGER.debug("Endpoint for POST /v1/svc/ldap.")
            # Get the data from the service.
            results = provider.search_ldap(body=body)
            search_response = json.loads(results.content)

            return http.JsonResponse(
                search_response, status=status.HTTP_200_OK, safe=False
            )
        except LDAPServiceError as err:
            return http.JsonResponse(data=err.message, status=err.status, safe=False)
