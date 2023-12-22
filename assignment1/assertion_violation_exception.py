from program.assertion import Assertion


class AssertionVialationException(Exception):
    assertion_statement: Assertion
    
    def __init__(self, assertion_statement: Assertion, *args: object) -> None:
        super().__init__(*args)
        self.assertion_statement = assertion_statement
        