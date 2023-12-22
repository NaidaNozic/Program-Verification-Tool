from program.expression import Expression
from program.statement import Statement


class Assignment(Statement):
    id: str
    expression: Expression
    __match_args__ = ('line', 'column', 'expression', 'id')
    
    def __init__(self, line: int, column: int, expression: Expression, id: str) -> None:
        super().__init__(line, column)
        self.id = id
        self.expression = expression

    def __str__(self) -> str:
        return 'Assignment({id} = {expression})'.format(
            id=self.id, 
            expression=self.expression.__str__()
            )
