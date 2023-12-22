from program.binary import Binary
from enum import Enum
from program.expression import Expression


class AndOrType(Enum):
    AND = 1
    OR = 2


class AndOr(Binary):
    type: AndOrType
    __match_args__ = ('line', 'column', 'left_expression', 'right_expression', 'type')

    def __init__(
            self, 
            line: int,
            column: int,
            left_expression: Expression, 
            right_expression: Expression,
            type: AndOrType
            ) -> None:
        super().__init__(line, column, left_expression, right_expression)
        self.type = type

    def __str__(self) -> str:
        return 'AndOr({left_expression}, {right_expression}, {type})'.format(
            left_expression=self.left_expression.__str__(),
            right_expression=self.right_expression.__str__(),
            type=self.type.name
        )
        