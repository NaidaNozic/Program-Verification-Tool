from program.binary import Binary
from enum import Enum
from program.expression import Expression

class ArithmeticType(Enum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4


class Arithmetic(Binary):
    type: ArithmeticType
    __match_args__ = ('line', 'column', 'left_expression', 'right_expression', 'type')

    def __init__(
            self, 
            line: int,
            column: int,
            left_expression: Expression, 
            right_expression: Expression, 
            type: ArithmeticType
            ) -> None:
        super().__init__(line, column, left_expression, right_expression)
        self.type = type

    def get_str(self) -> str:
        def get_str_type(type: ArithmeticType) -> str:
            match type:
                case ArithmeticType.ADD:
                    return '+'
                case ArithmeticType.SUBTRACT:
                    return '-'
                case ArithmeticType.MULTIPLY:
                    return '*'
                case ArithmeticType.DIVIDE:
                    return '/'
                
        return '{left_expression} {operator} {right_expression}'.format(
            left_expression=self.left_expression.get_str(), 
            operator=get_str_type(self.type), 
            right_expression=self.right_expression.get_str()
        )
    
    def __str__(self) -> str:
        return 'Arithmetic({left_expression}, {right_expression}, {type})'.format(
            left_expression=self.left_expression.__str__(),
            right_expression=self.right_expression.__str__(),
            type=self.type.name
        )
