"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Program Review Tool` API,
participating in the request/response cycle.
"""

from django.urls import path

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = []
