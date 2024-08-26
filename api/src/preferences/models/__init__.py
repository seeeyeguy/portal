"""
`Preferences` models module. Models conform to our data model and
provide access to Django migrations and ORM. These models help to
store and manage user preferences, including favorites, filter states,
etc. With these models, we hope to improve the user's experience and
make the application UI easier to navigate.
"""

from preferences.models.Favorite import Favorite
from preferences.models.QueryFilterState import QueryFilterState
