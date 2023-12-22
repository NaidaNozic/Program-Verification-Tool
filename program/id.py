from program.expression import Expression


class Id(Expression):
    id: str
    __match_args__ = ('line', 'column', 'id')

    def __init__(self, line: int, column: int, id: str) -> None:
        super().__init__(line, column)
        self.id = id

    def get_str(self) -> str:
        return self.id

    def __str__(self) -> str:
        return 'Id({id})'.format(id=self.id)
        