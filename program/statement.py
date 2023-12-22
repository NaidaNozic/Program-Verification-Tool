from program.node import Node
from program.expression import Expression


class Statement(Node):
    __match_args__ = ('line', 'column')

    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
