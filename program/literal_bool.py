from program.literal import Literal


class LiteralBool(Literal):
    value: bool
    __match_args__ = ('line', 'column', 'value')

    def __init__(self, line: int, column: int, value: bool) -> None:
        super().__init__(line, column)
        self.value = value

    def get_str(self) -> str:
        return 'true' if self.value else 'false'
    
    def __str__(self) -> str:
        return 'LiteralBool({value})'.format(value='true' if self.value else 'false')
