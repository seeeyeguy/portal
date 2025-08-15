"""
`Program Review Tool` `Program` review Tableau script file
that attempts to sign in to L3Harris Tableau server and store
the tokens in the cache.
"""

from program_review_tool.utils.review.tableau import cache_tableau_auth_tokens


def run() -> None:
    """
    Script function for authenticating with L3Harris
    Tableau server and storing the tokens in the cache.

    Accepts:
        * None

    Return:
        * None
    """

    cache_tableau_auth_tokens()
