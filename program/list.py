from program.expression import Expression


class List(Expression):
    expressions: list[Expression]
    __match_args__ = ('line', 'column', 'expressions')

    def __init__(self, line: int, column: int, expressions: list[Expression]):
        super().__init__(line, column)
        self.expressions = expressions

    def __str__(self):
        return 'List([{expressions}])'.format(
            expressions=', '.join([expression.__str__() for expression in self.expressions])
        )