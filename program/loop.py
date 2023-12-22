from program.expression import Expression
from program.statement import Statement


class Loop(Statement):
    expression: Expression
    invariant: Expression
    decreases: list[Expression] | None
    statement: Statement
    __match_args__ = ('line', 'column', 'expression', 'invariant', 'decreases', 'statement')

    def __init__(
            self, 
            line: int, 
            column: int, 
            expression: Expression, 
            invariant: Expression,
            decreases: list[Expression] | None, 
            statement: Statement
    ) -> None:
        super().__init__(line, column)
        self.expression = expression
        self.invariant = invariant
        self.decreases = decreases
        self.statement = statement

    def __str__(self) -> str:
        return 'Loop({expression}, {statement})'.format(
            expression=self.expression.__str__(),
            statement=self.statement.__str__()
        )
