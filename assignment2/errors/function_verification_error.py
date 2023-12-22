from assignment2.errors.verification_error import VerificationError


class FunctionVerificationError(VerificationError):
    id: str

    def __init__(self, id: str, line: int, column: int) -> None:
        super().__init__(line, column, 'Invalid function {id} on ({line},{column})'.format(
            id=id,
            line=line,
            column=column
        ))
        self.id = id

    def __eq__(self, other):
        return isinstance(
            other,
            FunctionVerificationError
        ) and other.id == self.id and other.line == self.line and other.column == self.column
