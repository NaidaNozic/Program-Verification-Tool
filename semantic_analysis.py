from antlr4 import FileStream, CommonTokenStream, InputStream
from antlr4_generated.ProgramLexer import ProgramLexer
from antlr4_generated.ProgramParser import ProgramParser
from program_builder import ProgramBuilder
from program.program import Program
from program.function import Function
from program.function_call import FunctionCall
from program.node import Node
from program.assignment import Assignment
from program.if_else import IfElse
from program.loop import Loop
from program.assertion import Assertion
from program.expression import Expression
from program.literal_int import LiteralInt
from program.literal_bool import LiteralBool
from program.id import Id
from program.parentheses import Parentheses
from program.negate import Negate
from program.negative import Negative
from program.arithmetic import Arithmetic
from program.compare import Compare, CompareType
from program.and_or import AndOr
from program.type import Type
from program.block import Block
from program.list import List
from program.list_get import ListGet
from program.length import Length
from program.forall import Forall
from program.exists import Exists
from program.implication import Implication


def build_parse_tree_from_str(program: str):
    input_stream = InputStream(program)
    program_lexer = ProgramLexer(input_stream)
    tokens = CommonTokenStream(program_lexer)
    program_parser = ProgramParser(tokens)
    return program_parser.program()


def build_parse_tree(file_path: str):
    file_stream = FileStream(file_path)
    program_lexer = ProgramLexer(file_stream)
    tokens = CommonTokenStream(program_lexer)
    program_parser = ProgramParser(tokens)
    return program_parser.program()


def build_program(parse_tree: ProgramParser.ProgramContext) -> Program | None:
    return parse_tree.accept(ProgramBuilder())


def build_type_error_message(line: int, column: int, message: str) -> str:
    return 'Type Error: {message}! ({line}, {column})'.format(
        message=message,
        line=line, 
        column=column
        )


def print_errors(errors: list[str]):
    if len(errors) == 0:
        return
    
    print('Errors:')
    for error in errors:
        print(error)


def get_type(expression: Expression, variables: dict[str, Type], errors: list[str]) -> Type | None:
    match expression:
        case LiteralInt(_, _, _):
            return Type.INT
        
        case LiteralBool(_, _, _):
            return Type.BOOL
        
        case Id(line, column, id):
            if id not in variables:
                errors.append(build_type_error_message(line, column, 'variable "{id}" did not exist'.format(id=id)))
                return None
            
            return variables[id]
        
        case Parentheses(_, _, expression):
            return get_type(expression, variables, errors)
        
        case Negate(line, column, expression):
            type = get_type(expression, variables, errors)

            if type is None:
                return None
            
            if type != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'negate expression requires its operand to be a bool'))
                return None
            
            return Type.BOOL
        
        case Negative(line, column, expression):
            type = get_type(expression, variables, errors)

            if type is None:
                return None
            
            if type != Type.INT:
                errors.append(build_type_error_message(line, column, 'negative expression requires its operand to be an integer'))
                return None
            
            return Type.INT
        
        case Arithmetic(line, column, left_expression, right_expression, _):
            left_expression_type = get_type(left_expression, variables, errors)
            if left_expression_type is None:
                return None
            
            right_expression_type = get_type(right_expression, variables, errors)
            if right_expression_type is None:
                return None

            if left_expression_type != Type.INT or right_expression_type != Type.INT:
                errors.append(build_type_error_message(line, column, 'arithmetic expression requires its operands to be integers'))
                return None
            
            return Type.INT
        
        case Compare(line, column, left_expression, right_expression, type):
            left_expression_type = get_type(left_expression, variables, errors)
            if left_expression_type is None:
                return None
            
            right_expression_type = get_type(right_expression, variables, errors)
            if right_expression_type is None:
                return None

            if left_expression_type != right_expression_type:
                errors.append(build_type_error_message(line, column, 'compare expression requires its operands to have the same type'))
                return None

            if left_expression_type != Type.INT and type != CompareType.EQUAL and type != CompareType.NOT_EQUAL:
                errors.append(build_type_error_message(line, column, 'compare expression requires its operands to be integers'))
                return None
            
            return Type.BOOL
        
        case AndOr(line, column, left_expression, right_expression, _):
            left_expression_type = get_type(left_expression, variables, errors)
            if left_expression_type is None:
                return None
            
            right_expression_type = get_type(right_expression, variables, errors)
            if right_expression_type is None:
                return None
            
            if left_expression_type != Type.BOOL or right_expression_type != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'and / or expression requires its operands to be bool'))
                return None
            
            return Type.BOOL

        case List(_, _, _):
            return Type.LIST_INT

        case ListGet(_, _, _, _) | Length(_, _, _):
            return Type.INT

        case Implication(line, column, left_expression, right_expression):
            left_expression_type = get_type(left_expression, variables, errors)
            if left_expression_type is None:
                return None

            right_expression_type = get_type(right_expression, variables, errors)
            if right_expression_type is None:
                return None

            if left_expression_type != Type.BOOL or right_expression_type != Type.BOOL:
                errors.append('implication expression requires its operands to be bool')
                return None

            return Type.BOOL

        case Forall(line, column, expression, ids) | Exists(line, column, expression, ids):
            quantifier_variables = {id: Type.INT for id in ids}
            type = get_type(expression, variables | quantifier_variables, errors)

            if type is None:
                return None

            if type != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'quantifier expression requires its operand to be bool'))

            return Type.BOOL
      

def check_function(
        function: Function, 
        function_call: FunctionCall | None
) -> tuple[dict[str, Type], dict[str, Expression] | None, list[str]]:
    variables = {}
    errors = []

    for parameter in function.parameters:
        if parameter[0] in variables:
            errors.append(build_type_error_message(
                function.line, 
                function.column, 
                'parameter {parameter} was declared more than once'.format(paremeter=parameter[0])
            ))
            continue
        variables[parameter[0]] = parameter[1]

    if function_call is None:
        return variables, None, errors
    
    if function_call.id != function.id:
        errors.append(build_type_error_message(
            function_call.line, 
            function_call.column, 
            'unknown function {function}'.format(function=function_call.id)
        ))
    
    if len(function_call.arguments) != len(function.parameters):
        errors.append(build_type_error_message(0, 0, 'the {function} function call includes {arguments} for {parameters}'.format(
            function=function_call.id, 
            arguments=str(len(function_call.arguments)) + (' argument' if len(function_call.arguments) == 1 else ' arguments'),
            parameters=str(len(function.parameters)) + (' parameter' if len(function.parameters) == 1 else ' parameters')
        )))
        return variables, None, errors

    variables_expressions = {}
    for i in range(len(function_call.arguments)):
        parameter_type = function.parameters[i][1]
        argument_type = get_type(function_call.arguments[i], variables, errors)

        if argument_type is None:
            return variables, variables_expressions, errors
        
        if argument_type != parameter_type:
            errors.append(build_type_error_message(0, 0, 'the {function} function call requires a {parameter_type} for parameter {parameter}, but {argument_type} given'.format(
                function=function.id,
                parameter_type='int' if parameter_type == Type.INT else 'bool',
                parameter=function.parameters[i][0],
                argument_type='int' if argument_type == Type.INT else 'bool'
            )))
        variables_expressions[function.parameters[i][0]] = function_call.arguments[i]

    return variables, variables_expressions, errors


def check_types(program: Node, variables: dict[str, Type] = {}, errors: list[str] = []) -> tuple[dict[str, Type], list[str]]:
    match program:
        case Program(_, _, function, _):
            check_types(function, variables, errors)
        
        case Function(line, column, id, _, precondition, postcondition, statement):
            if precondition is not None and get_type(precondition, variables, errors) != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'function {id} requires its precondition to be bool'.format(id=id)))
            
            if postcondition is not None and get_type(postcondition, variables, errors) != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'function {id} requires its postcondition to be bool'.format(id=id)))

            check_types(statement, variables, errors)

        case Block(_, _, statements):
            for statement in statements:
                check_types(statement, variables, errors)

        case Assignment(line, column, expression, id):
            type = get_type(expression, variables, errors)

            if type is not None and id not in variables:
                variables[id] = type

            if type is not None and variables[id] != type:
                errors.append(build_type_error_message(line, column, '{expression_type} can not be assigned to variable {id} of type {id_type}'.format(
                    expression_type=type.name, 
                    id=id,
                    id_type=variables[id].name
                    )))

        case IfElse(line, column, expression, then_statement, else_statement):
            type = get_type(expression, variables, errors)

            if type is not None and type != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'if statement requires a bool condition'))

            check_types(then_statement, variables, errors)

            if else_statement is not None:
                check_types(else_statement, variables, errors)

        case Loop(line, column, expression, invariant, decreases, statement):
            if invariant is not None and get_type(invariant, variables, errors) != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'while statement requires its invariant to be bool'))

            type = get_type(expression, variables, errors)
            
            if type is not None and type != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'while statement requires a bool condition'))
                check_types(statement, variables, errors)

        case Assertion(line, column, expression):
            type = get_type(expression, variables, errors)

            if type is not None and type != Type.BOOL:
                errors.append(build_type_error_message(line, column, 'assert statement requires a bool parameter'))
    
    return variables, errors

def check(program: Program | None) -> tuple[dict[str, Type], dict[str, Expression] | None, list[str]]:
    if program is None:
        return None
    
    variables, variables_expressions, errors = check_function(program.function, program.function_call)
    print_errors(errors)

    if len(errors) != 0:
        return None
    
    variables, errors = check_types(program.function.statement, variables, errors)
    print_errors(errors)

    if len(errors) != 0:
        return None

    variables, errors = check_types(program, variables, errors)
    print_errors(errors)

    if len(errors) != 0:
        return None
    
    return variables, variables_expressions, errors