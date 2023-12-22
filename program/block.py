from program.statement import Statement


class Block(Statement):
    statements: list[Statement]
    __match_args__ = ('line', 'column', 'statements')

    def __init__(self, line: int, column: int, statements: list[Statement]):
        super().__init__(line, column)
        self.statements = statements

    def __str__(self):
        return '[{statements}]'.format(statements=[statement.__str__() for statement in self.statements])
