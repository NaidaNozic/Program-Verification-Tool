from program.expression import Expression


class Length(Expression):
    id: str
    __match_args__ = ('line', 'column', 'id')

    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column)
        self.id = id
