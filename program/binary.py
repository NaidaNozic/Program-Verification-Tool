from program.expression import Expression


class Binary(Expression):
    left_expression: Expression
    right_expression: Expression
    __match_args__ = ('line', 'column', 'left_expression', 'right_expression')

    def __init__(self, line: int, column: int, left_expression: Expression, right_expression: Expression) -> None:
        super().__init__(line, column)
        self.left_expression = left_expression
        self.right_expression = right_expression
