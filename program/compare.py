from program.binary import Binary
from enum import Enum
from program.expression import Expression


class CompareType(Enum):
    EQUAL = 1
    NOT_EQUAL = 2
    GREATER = 3
    LESS = 4
    GREATER_EQUAL = 5
    LESS_EQUAL = 6


class Compare(Binary):
    type: CompareType
    __match_args__ = ('line', 'column', 'left_expression', 'right_expression', 'type')

    def __init__(
            self, 
            line: int,
            column: int,
            left_expression: Expression, 
            right_expression: Expression,
            type: CompareType
            ) -> None:
        super().__init__(line, column, left_expression, right_expression)
        self.type = type

    def get_str(self) -> str:
        def get_str_type(type: CompareType) -> str:
            match type:
                case CompareType.EQUAL:
                    return '=='
                case CompareType.NOT_EQUAL:
                    return '!='
                case CompareType.GREATER:
                    return '>'
                case CompareType.LESS:
                    return '<'
                case CompareType.GREATER_EQUAL:
                    return '>='
                case CompareType.LESS_EQUAL:
                    return '<='
                
        return '{left_expression} {operator} {right_expression}'.format(
            left_expression=self.left_expression.get_str(),
            operator=get_str_type(self.type),
            right_expression=self.right_expression.get_str()
        )
    
    def __str__(self) -> str:
        return 'Compare({left_expression}, {right_expression}, {type})'.format(
            left_expression=self.left_expression.__str__(),
            right_expression=self.right_expression.__str__(),
            type=self.type.name
        )
        