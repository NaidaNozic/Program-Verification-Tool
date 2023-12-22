from program.statement import Statement
from program.expression import Expression


class Assertion(Statement):
    expression: Expression
    __match_args__ = ('line', 'column', 'expression')

    def __init__(self, line: int, column: int, expression: Expression) -> None:
        super().__init__(line, column)
        self.expression = expression

    def __str__(self) -> str:
        return 'Assertion({expression})'.format(expression=self.expression.__str__())
    