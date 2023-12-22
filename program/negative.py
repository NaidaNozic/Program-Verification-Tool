from program.unary import Unary


class Negative(Unary):
    def get_str(self) -> str:
        return '-' + self.expression.get_str()
    
    def __str__(self) -> str:
        return 'Negative({expression})'.format(expression=self.expression.__str__())
