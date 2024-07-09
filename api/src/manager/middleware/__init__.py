"""
Custom middleware module for PMX applications. Middleware allows
developers to manipulate the objects in the request/response cycle,
adding, modifying, or even removing data as needed through function/modules
installed in `manager.settings.MIDDLEWARE`. It is important to note that
middleware is run top-down, bottom-up for the request and response cyle
respectively so we must carefully consider the placement of our middleware
in `manager.settings.MIDDLEWARE`.  
"""

from manager.middleware.DevelopmentAuthenticationMiddleware import (
    DevelopmentAuthenticationMiddleware,
)
