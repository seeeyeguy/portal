"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Request` API, participating
in the request/response cycle.
"""

from django.urls import path

from request import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    path("request", views.Request.as_view(), name="request.request")
]
