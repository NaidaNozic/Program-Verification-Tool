from assignment2.errors.function_verification_error import FunctionVerificationError
from assignment2.errors.invariant_verification_error import InvariantVerificationError, InvariantVerificationErrorType
from assignment2.errors.termination_verification_error import TerminationVerificationError, TerminationVerificationErrorType
from program.and_or import AndOr, AndOrType
from program.arithmetic import Arithmetic, ArithmeticType
from program.assertion import Assertion
from program.assignment import Assignment
from program.block import Block
from program.forall import Forall
from program.exists import Exists
from program.implication import Implication
from program.list_get import ListGet
from program.list_set import ListSet
from program.loop import Loop
from program.compare import Compare, CompareType
from program.id import Id
from program.if_else import IfElse
from program.literal_bool import LiteralBool
from program.literal_int import LiteralInt
from program.negate import Negate
from program.negative import Negative
from program.parentheses import Parentheses
from program.program import Program
from program.type import Type
from program.function import Function
from assignment2.errors.verification_error import VerificationError
import z3

def get_z3_sort(type):
    if type == Type.INT or type == Type.LIST_INT:
        return z3.IntSort()
    elif type == Type.BOOL:
        return z3.BoolSort()
    else:
        raise ValueError(f"Unsupported type: {type}")

    
def prove_formula(formula):
    solver = z3.Solver()
    solver.add(z3.Not(formula))
    return str(solver.check()) == "unsat"


def verify(program: Program, variables: dict[str, Type], errors: list[VerificationError]):
    if program is None or program.function is None:
        return None
    verify_function(program.function, variables, errors)

def verify_function(function: Function, variables: dict[str, Type], errors: list[VerificationError]):
    precondition_z3 = get_z3_expr(function.precondition, variables)
    postcondition_z3 = get_z3_expr(function.postcondition, variables)
    
    postcondition_z3 = verify_statement(function.statement, variables, [postcondition_z3, True], errors)

    if (prove_formula(z3.Implies(precondition_z3,postcondition_z3[0])) and prove_formula(postcondition_z3[1])) is False:
        errors.append(FunctionVerificationError(function.id, function.line, function.column))

def verify_loop(loop: Loop, variables, postcondition_z3, errors):
    condition = get_z3_expr(loop.expression, variables)
    invariant = get_z3_expr(loop.invariant, variables)

    variants1, variants2, termination_premise = process_decreases(loop.decreases, variables, loop.line, loop.column)

    recursive_condition1 = verify_statement(loop.statement, variables, [invariant, postcondition_z3[1]], errors) 

    invariance_premise = True
    postcondition_premise = True
    invariance_premise = z3.Implies(z3.And(condition,invariant), recursive_condition1[0])
    postcondition_premise = z3.Implies(z3.And(z3.Not(condition),invariant), postcondition_z3[0])

    if prove_formula(postcondition_premise) is False:
        errors.append(InvariantVerificationError(loop.line, loop.column, InvariantVerificationErrorType.POSTCONDITION_MISMATCH))

    if prove_formula(invariance_premise) is False:
        errors.append(InvariantVerificationError(loop.line, loop.column, InvariantVerificationErrorType.NOT_AN_INVARIANT))
    else:
        if loop.decreases is not None:
            recursive_condition2 = verify_statement(loop.statement, variables, [z3.And(invariant, variants2), postcondition_z3[1]], errors) 
            invariance_premise = z3.Implies(z3.And(condition,invariant,variants1), recursive_condition2[0])
            if prove_formula(invariance_premise) is False:
                errors.append(TerminationVerificationError(loop.line, loop.column, TerminationVerificationErrorType.INVALID))

    if loop.decreases is not None:
        termination_premise = z3.Implies(z3.And(condition,invariant), termination_premise)
        if prove_formula(termination_premise) is False:
            errors.append(TerminationVerificationError(loop.line, loop.column, TerminationVerificationErrorType.NOT_BOUNDED))

    return [invariant, z3.And(postcondition_z3[1], invariance_premise, postcondition_premise, termination_premise)]

def verify_statement(statement, variables, postcondition_z3, errors):
    match statement:
        case Block(_, _, statements):
            for statement in reversed(statements):
                postcondition_z3 = verify_statement(statement, variables, postcondition_z3, errors)

        case Assignment(_, _, expression, id):
            left = z3.Const(id, get_z3_sort(variables[id]))
            right = get_z3_expr(expression, variables)
            postcondition_z3 =  [z3.substitute(postcondition_z3[0], (left, right)), postcondition_z3[1]]

        case IfElse(_, _, expression, then_statement, else_statement):
            expression = get_z3_expr(expression, variables)
            else_condition = verify_statement(else_statement, variables, postcondition_z3, errors)
            then_condition = verify_statement(then_statement, variables, postcondition_z3, errors)
            
            postcondition_z3 = [z3.Or(z3.And(expression, then_condition[0]), z3.And(z3.Not(expression), else_condition[0])), 
                                z3.And(then_condition[1], else_condition[1])]
            
        case Assertion(_, _, expression):
            assertion_z3 = get_z3_expr(expression, variables)
            postcondition_z3 = [z3.And(postcondition_z3[0], assertion_z3), postcondition_z3[1]]

        case ListSet(_, _, id, index_expression, set_expression):
            array_name = z3.Array(str(id), z3.IntSort(), get_z3_sort(variables[id]))
            index_expr = get_z3_expr(index_expression, variables)
            set_expr = get_z3_expr(set_expression, variables)
            
            updated_array = z3.Store(array_name, index_expr, set_expr)
            substitution = z3.substitute(postcondition_z3[0],(array_name, updated_array))
            return [substitution, postcondition_z3[1]]
            
        case Loop():
            postcondition_z3 = verify_loop(statement, variables, postcondition_z3, errors)

    return postcondition_z3

def get_z3_expr(expression, variables):
    match expression:
        case Parentheses(_, _, expression):
            return get_z3_expr(expression, variables)
            
        case LiteralInt(_, _, value):
            return z3.IntVal(value)
        
        case LiteralBool(_, _, value):
            return z3.BoolVal(value)
        
        case Id(_, _, id):
            if id in variables:
                return z3.Const(id, get_z3_sort(variables[id]))
            else:
                return z3.Const(id, z3.IntSort())
            
        case ListGet(_, _, expression, id):
            array_name = z3.Array(str(id), z3.IntSort(), get_z3_sort(variables[id]))
            return z3.Select(array_name, get_z3_expr(expression, variables))
            
        case Compare(_, _, left, right, compare_type):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            x = z3.Int('x')
            match compare_type:
                case CompareType.EQUAL:
                    return left_z3 == right_z3
                case CompareType.NOT_EQUAL:
                    return left_z3 != right_z3
                case CompareType.GREATER:
                    return left_z3 > right_z3
                case CompareType.LESS:
                    return left_z3 < right_z3
                case CompareType.GREATER_EQUAL:
                    return left_z3 >= right_z3
                case CompareType.LESS_EQUAL:
                    return left_z3 <= right_z3
                
        case AndOr(_, _, left, right, AndOrType.AND):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            return z3.And(left_z3, right_z3)

        case AndOr(_, _, left, right, AndOrType.OR):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            return z3.Or(left_z3, right_z3)
        
        case Negate(_, _, operand):
            operand_z3 = get_z3_expr(operand, variables)
            return z3.Not(operand_z3)
        
        case Negative(_, _, operand):
            operand_z3 = get_z3_expr(operand, variables)
            return -operand_z3
        
        case Arithmetic(_, _, left, right, ArithmeticType.ADD):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            return left_z3 + right_z3

        case Arithmetic(_, _, left, right, ArithmeticType.SUBTRACT):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            return left_z3 - right_z3

        case Arithmetic(_, _, left, right, ArithmeticType.MULTIPLY):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            return left_z3 * right_z3

        case Arithmetic(_, _, left, right, ArithmeticType.DIVIDE):
            left_z3 = get_z3_expr(left, variables)
            right_z3 = get_z3_expr(right, variables)
            return left_z3 / right_z3
        
        case Implication(_, _, left_expression, right_expression):
            left_z3 = get_z3_expr(left_expression, variables)
            right_z3 = get_z3_expr(right_expression, variables)
            return z3.Implies(left_z3, right_z3)
        
        case Forall(_, _, expression, ids):
            quantifier_variables = {id: Type.INT for id in ids}
            z3_expression = get_z3_expr(expression, variables | quantifier_variables)
            return z3.ForAll([z3.Const(id, get_z3_sort(quantifier_variables[id])) for id in ids], z3_expression)

        case Exists(_, _, expression, ids):
            quantifier_variables = {id: Type.INT for id in ids}
            z3_expression = get_z3_expr(expression, variables | quantifier_variables)
            return z3.Exists([z3.Const(id, get_z3_sort(quantifier_variables[id])) for id in ids], z3_expression)


def process_decreases(decreases, variables, line, column):
    smaller_variant_cond = False
    equal_variant_cond = True
    termination_premise = True

    if decreases is not None:
        smaller_variant_cond = z3.Or(smaller_variant_cond, get_z3_expr(decreases[0], variables) < z3.Int(f'n({line},{column},0)'))
        for i in range(1,len(decreases)):
            tmp = True

            for j in range(0,i):
                variant = get_z3_expr(decreases[j], variables)
                termination_premise = z3.And(termination_premise, variant >= 0)
                tmp = z3.And(tmp, variant == z3.Int(f'n({line},{column},{j})'))
                equal_variant_cond = tmp

            tmp = z3.And(tmp, get_z3_expr(decreases[i], variables) < z3.Int(f'n({line},{column},{i})'))
            smaller_variant_cond = z3.Or(smaller_variant_cond, tmp)

        last_variant = get_z3_expr(decreases[len(decreases)-1], variables)
        equal_variant_cond = z3.And(equal_variant_cond, last_variant == z3.Int(f'n({line},{column},{len(decreases)-1})'))
        termination_premise = z3.And(termination_premise, last_variant >= 0)

    return equal_variant_cond, smaller_variant_cond, termination_premise