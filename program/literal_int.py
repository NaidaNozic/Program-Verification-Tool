from program.literal import Literal


class LiteralInt(Literal):
    value: int
    __match_args__ = ('line', 'column', 'value')

    def __init__(self, line: int, column: int, value: int) -> None:
        super().__init__(line, column)
        self.value = value

    def get_str(self) -> str:
        return str(self.value)
    
    def __str__(self) -> str:
        return 'LiteralInt({value})'.format(value=str(self.value))
