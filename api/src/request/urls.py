"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Request` API, participating
in the request/response cycle.
"""

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = []
