from program.unary import Unary
from program.expression import Expression
from program.list_set import ListSet


class ListGet(Unary):
    id: str
    list_sets: list[ListSet]
    __match_args__ = ('line', 'column', 'expression', 'id', 'list_sets')

    def __init__(self, line: int, column: int, expression: Expression, id: str, list_sets: list[ListSet] = []):
        super().__init__(line, column, expression)
        self.id = id
        self.list_sets = list_sets

    def __str__(self):
        return 'ListGet({id}[{expression}])'.format(id=self.id, expression=self.expression.__str__())
