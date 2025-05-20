"""
`Program Review Tool` `Program` review Tableau script file
that attempts to sign in to L3Harris Tableau server and store
the token in the cache.
"""

from program_review_tool.utils.review.tableau import cache_tableau_auth_token


def run() -> None:
    """
    Script function for authenticating with L3Harris
    Tableau server and storing the token in the cache.

    Accepts:
        * None

    Return:
        * None
    """

    cache_tableau_auth_token()
