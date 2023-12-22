from program.unary import Unary
from program.expression import Expression


class Quantifier(Unary):
    ids: list[str]
    __match_args__ = ('line', 'column', 'expression', 'ids')

    def __init__(self, line: int, column: int, expression: Expression, ids: list[str]):
        super().__init__(line, column, expression)
        self.ids = ids
