from program.statement import Statement
from program.expression import Expression


class ListSet(Statement):
    id: str
    index_expression: Expression
    set_expression: Expression
    __match_args__ = ('line', 'column', 'id', 'index_expression', 'set_expression')

    def __init__(self, line: int, column: int, id: str, index_expression: Expression, set_expression: Expression):
        super().__init__(line, column)
        self.id = id
        self.index_expression = index_expression
        self.set_expression = set_expression

    def __str__(self):
        return 'ListSet({id}[{index_expression}] = {set_expression})'.format(
            id=self.id,
            index_expression=self.index_expression.__str__(),
            set_expression=self.set_expression.__str__()
        )