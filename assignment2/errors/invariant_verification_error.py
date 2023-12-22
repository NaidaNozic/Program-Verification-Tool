from assignment2.errors.verification_error import VerificationError
from enum import Enum

class InvariantVerificationErrorType(Enum):
    POSTCONDITION_MISMATCH = 1,
    NOT_AN_INVARIANT = 2


class InvariantVerificationError(VerificationError):
    type: InvariantVerificationErrorType

    def __init__(self, line: int, column: int, type: InvariantVerificationErrorType):
        super().__init__(line, column, 'Could not prove invariant for loop on ({line},{column}): {type}'.format(
            type=type.name,
            line=line,
            column=column
        ))
        self.type = type

    def __eq__(self, other):
        return isinstance(
            other,
            InvariantVerificationError
        ) and other.line == self.line and other.column == self.column and other.type == self.type