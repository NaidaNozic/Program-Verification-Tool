from program.program import Program
from program.expression import Expression
from program.literal_int import LiteralInt
from program.literal_bool import LiteralBool
from program.id import Id
from program.parentheses import Parentheses
from program.negate import Negate
from program.negative import Negative
from program.arithmetic import Arithmetic, ArithmeticType
from program.compare import Compare, CompareType
from program.and_or import AndOr, AndOrType
from program.statement import Statement
from program.assignment import Assignment
from program.if_else import IfElse
from program.loop import Loop
from program.assertion import Assertion
from program.write import Write
from program.block import Block
from assignment1.assertion_violation_exception import AssertionVialationException
from semantic_analysis import print_errors


def interpret_expression(expression: Expression, environment: dict[str, any]) -> any:
    match expression:
        case LiteralInt(_, _, value) | LiteralBool(_, _, value):
            return value
        
        case Id(_, _, id):
            return environment[id]
        
        case Parentheses(_, _, expression):
            return interpret_expression(expression, environment)
        
        case Negate(_, _, expression):
            return not interpret_expression(expression, environment)
        
        case Negative(_, _, expression):
            return - interpret_expression(expression, environment)
        
        case Arithmetic(_, _, left_expression, right_expression, type):
            match type:
                case ArithmeticType.ADD:
                    return interpret_expression(left_expression, environment) + interpret_expression(right_expression, environment)
                case ArithmeticType.SUBTRACT:
                    return interpret_expression(left_expression, environment) - interpret_expression(right_expression, environment)
                case ArithmeticType.MULTIPLY:
                    return interpret_expression(left_expression, environment) * interpret_expression(right_expression, environment)
                case ArithmeticType.DIVIDE:
                    return interpret_expression(left_expression, environment) / interpret_expression(right_expression, environment)
                
        case Compare(_, _, left_expression, right_expression, type):
            match type:
                case CompareType.EQUAL:
                    return interpret_expression(left_expression, environment) == interpret_expression(right_expression, environment)
                case CompareType.NOT_EQUAL:
                    return interpret_expression(left_expression, environment) != interpret_expression(right_expression, environment)
                case CompareType.GREATER:
                    return interpret_expression(left_expression, environment) > interpret_expression(right_expression, environment)
                case CompareType.LESS:
                    return interpret_expression(left_expression, environment) < interpret_expression(right_expression, environment)
                case CompareType.GREATER_EQUAL:
                    return interpret_expression(left_expression, environment) >= interpret_expression(right_expression, environment)
                case CompareType.LESS_EQUAL:
                    return interpret_expression(left_expression, environment) <= interpret_expression(right_expression, environment)
        
        case AndOr(_, _, left_expression, right_expression, type):
            match type:
                case AndOrType.AND:
                    return interpret_expression(left_expression, environment) and interpret_expression(right_expression, environment)
                case AndOrType.OR:
                    return interpret_expression(left_expression, environment) or interpret_expression(right_expression, environment)


def interpret_statements(statements: list[Statement], environment: dict[str, any], interpret_statement_callback = None):
        for statement in statements:
            interpret_statement(statement, environment, interpret_statement_callback)


def interpret_statement(statement: Statement, environment: dict[str, any], interpret_statement_callback = None):
    match statement:
        case Assignment(_, _, expression, id):
            environment[id] = interpret_expression(expression, environment)

        case Block(_, _, statements):
            interpret_statements(statements, environment, interpret_statement_callback)

        case IfElse(_, _, expression, then_statement, else_statement):
            if interpret_expression(expression, environment):
                interpret_statement(then_statement, environment, interpret_statement_callback)
                return
            
            if else_statement is not None:
                interpret_statement(else_statement, environment, interpret_statement_callback)

        case Loop(_, _, expression, _, _, statement):
            while interpret_expression(expression, environment):
                interpret_statement(statement, environment, interpret_statement_callback)

        case Assertion(_, _, expression) as assertion_statement:
            if not interpret_expression(expression, environment):
                raise AssertionVialationException(assertion_statement)
            
        case Write(_, _, expression):
            print(str(interpret_expression(expression, environment)))
    
    if interpret_statement_callback is not None:
        interpret_statement_callback(statement)


def interpret(program: Program, variables_expressions: dict[str, Expression], errors: list[str], interpret_statement_callback = None):
    try:
        interpret_statement(
            program.function.statement,
            {variable_id : interpret_expression(expression, {}) for variable_id, expression in variables_expressions.items()},
            interpret_statement_callback
        )
    except AssertionVialationException as assertionViolationException:
        errors.append('Assertion violation! ({line}, {column})'.format(
            line=assertionViolationException.assertion_statement.line, 
            column=assertionViolationException.assertion_statement.column
        ))

    print_errors(errors)