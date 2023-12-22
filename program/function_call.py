from program.node import Node
from program.expression import Expression


class FunctionCall(Node):
    id: str
    arguments: list[Expression]

    def __init__(self, line: int, column: int, id: str, arguments: list[Expression]) -> None:
        super().__init__(line, column)
        self.id = id
        self.arguments = arguments
