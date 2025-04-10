"""
`Program Review Tool` view module. Views handle requests to process
additions/deletions/modifications/queries of `Program Review Tool` programs
and portfolios. These objects help the generate powerpoint review
templates that provide consolidated insights into the health of
programs.
"""

from .program.program import Program  # ordered to prevent potential circular dependency
from .portfolio.portfolio import Portfolio
