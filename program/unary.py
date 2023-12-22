from program.expression import Expression


class Unary(Expression):
    expression: Expression
    __match_args__ = ('line', 'column', 'expression')

    def __init__(self, line: int, column: int, expression: Expression) -> None:
        super().__init__(line, column)
        self.expression = expression
