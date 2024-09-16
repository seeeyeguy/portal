"""
Type module for urlconfig. This module provides
custom types for the urls module for each Django
application.
"""

from typing import List, Union

from django.urls import URLPattern, URLResolver

PathPattern = Union[URLPattern, URLResolver]

PathPatternList = List[PathPattern]
