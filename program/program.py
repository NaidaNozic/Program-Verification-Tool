from program.node import Node
from program.function import Function
from program.function_call import FunctionCall

class Program(Node):
    function: Function
    function_call: FunctionCall | None
    __match_args__ = ('line', 'column', 'function', 'function_call')

    def __init__(
            self, 
            line: int, 
            column: int, 
            function: Function, 
            function_call: FunctionCall | None
    ) -> None:
        super().__init__(line, column)
        self.function = function
        self.function_call = function_call

    def __str__(self) -> str:
        return 'Program({function})'.format(function=self.function.__str__())
