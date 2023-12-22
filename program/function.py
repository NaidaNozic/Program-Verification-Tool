from program.node import Node
from program.statement import Statement
from program.type import Type
from program.expression import Expression


FunctionParameter = tuple[str, Type]


class Function(Node):
    id: str
    parameters: list[FunctionParameter]
    precondition: Expression
    postcondition: Expression
    statement: Statement
    __match_args__ = ('line', 'column', 'id', 'parameters', 'precondition', 'postcondition', 'statement')

    def __init__(
            self, 
            line: int, 
            column: int, 
            id: str, 
            parameters: list[FunctionParameter], 
            precondition: Expression, 
            postcondition: Expression, 
            statement: Statement
    ) -> None:
        super().__init__(line, column)
        self.id = id
        self.parameters = parameters
        self.precondition = precondition
        self.postcondition = postcondition
        self.statement = statement

    def __str__(self):
        return 'Function({statement})'.format(statement=self.statement.__str__())
