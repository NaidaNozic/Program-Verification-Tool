from program.expression import Expression
from program.statement import Statement


class IfElse(Statement):
    expression: Expression
    then_statement: Statement
    else_statement: Statement | None
    __match_args__ = ('line', 'column', 'expression', 'then_statement', 'else_statement')

    def __init__(
            self, 
            line: int,
            column: int,
            expression: Expression, 
            then_statement: Statement,
            else_statement: Statement
            ) -> None:
        super().__init__(line, column)
        self.expression = expression
        self.then_statement = then_statement
        self.else_statement = else_statement

    def __str__(self) -> str:
        return 'IfElse({expression}, [{then_statement}], [{else_statement}])'.format(
            expression=self.expression.__str__(),
            then_statement=self.then_statement.__str__(),
            else_statement=self.else_statement.__str__() if self.else_statement is not None else ''
        )
