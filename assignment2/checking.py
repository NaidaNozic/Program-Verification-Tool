from program.program import Program
from assignment2.verification import verify
from program.program import Program
from assignment2.errors.verification_error import VerificationError

def print_errors(errors: list[VerificationError]):
    if len(errors) == 0:
        return
    
    print('Errors:')
    for error in errors:
        print(error)


def run(program: Program, variables: dict[str]):
    errors = []
    verify(program, variables, errors)
    print_errors(errors)
    