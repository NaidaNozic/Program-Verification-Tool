class VerificationError:
    line: int
    column: int
    message: str

    def __init__(self, line: int, column: int, message: str) -> None:
        self.line = line
        self.column = column
        self.message = message

    def __str__(self) -> str:
        return self.message
