"""
BI Portal `Request` view module. Views handle requests to process
additions/modifications/queries of BI Portal directory resources through
the request workflow.
"""

from .disposition.disposition import Disposition
from .request import Request, RequestNotification
