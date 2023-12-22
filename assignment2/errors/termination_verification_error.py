from assignment2.errors.verification_error import VerificationError
from enum import Enum


class TerminationVerificationErrorType(Enum):
    NOT_BOUNDED = 1
    INVALID = 2


class TerminationVerificationError(VerificationError):
    type: TerminationVerificationErrorType

    def __init__(self, line: int, column: int, type: TerminationVerificationErrorType):
        super().__init__(line, column, 'Can not prove termination for loop on ({line},{column}): {type}'.format(
            type=type.name,
            line=line,
            column=column
        ))
        self.type = type

    def __eq__(self, other):
        return isinstance(
            other,
            TerminationVerificationError
        ) and other.line == self.line and other.column == self.column and other.type == self.type
