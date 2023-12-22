from program.program import Program
from program.statement import Statement
from program.expression import Expression
from assignment1.interpreting import interpret
from assignment1.lock_tree.lock_tree_call import LockTreeCall
from assignment1.instrumentation import instrument
from assignment1.lock_tree.algorithm import check
from assignment1.lock_tree.warnings.warning import Warning


def print_warnins(warnings: list[Warning]):
    if len(warnings) == 0:
        return
    
    print('Warnings:')
    for warning in warnings:
        print(warning)


def interpret_statement_callback(statement: Statement, algorithm_calls: list[LockTreeCall]):
    match statement:
        case LockTreeCall(_, _, _, _) as algorithm_call:
            algorithm_calls.append(algorithm_call)


def run(programs: tuple[tuple[Program, dict[str, Expression], list[Warning]]]):
    programs_algorithm_calls = []
    for i in range(len(programs)):
        program = instrument(programs[i][0])
        algorithm_calls = []
        interpret(
            program, 
            programs[i][1], 
            programs[i][2],
            lambda statement: interpret_statement_callback(statement, algorithm_calls)
        )
        programs_algorithm_calls.append(('thread-' + str(i + 1), algorithm_calls))
    
    warnings = []
    check(programs_algorithm_calls, warnings)
    print_warnins(warnings)
    