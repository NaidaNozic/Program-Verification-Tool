from program.unary import Unary


class Negate(Unary):
    def get_str(self) -> str:
        return '!({expression})'.format(expression=self.expression.get_str())

    def __str__(self) -> str:
        return 'Negate({expression})'.format(expression=self.expression.__str__())
