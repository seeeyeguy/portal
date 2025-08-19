"""
`ProgramMember` module. `ProgramMember` represents a team
member for a `Program`, designating their role as well as
the status of that role on the `Program`. `ProgramMember`s
help to execute the `Program` and drive forward its objectives.
Each `User`s role and active status must be unique on a `Program`
(i.e. a `User` cannot have duplicate active roles on the same
`Program`).
"""

from .ProgramMember import ProgramMember
