"""
`Tag` module. `Tag` represents a set of arbitrary
labels that may be used to provide some metadata
about a resource. A `Tag` may also be used to categorize,
group and filter resources. As a `Tag`'s label is an
arbitrary string, we need the help of the `Tag` module to
provide validation, and eliminate redundancies.
"""

from directory.models.Tag.Tag import Tag
