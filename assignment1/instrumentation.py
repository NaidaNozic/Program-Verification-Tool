from program.assignment import Assignment
from program.if_else import IfElse
from program.loop import Loop
from program.node import Node
from program.program import Program
from program.function import Function
from program.block import Block
from program.lock import Lock
from program.unlock import Unlock
from assignment1.lock_tree.lock_tree_call import LockTreeCall, LockTreeCallType

        
def instrument_types(program: Node) -> Program:
    match program:
        case Program(line, column, function, function_call):
            new_function = instrument_types(function)
            return Program(line, column, new_function, function_call)

        case Function(line, column, id, parameters, precondition, postcondition, statement):
            new_statement = instrument_types(statement)
            return Function(line, column, id, parameters, precondition, postcondition, new_statement)

        case Block(line, column, statements):

            new_statements = []
            for statement in statements:
                new_statements.append(instrument_types(statement))
            return Block(line, column, new_statements)
        
        case IfElse(line, column, expression, then_statement, else_statement):
    
            then_statement = instrument_types(then_statement)

            if else_statement is not None:
                else_statement = instrument_types(else_statement)

            return IfElse(line, column, expression, then_statement, else_statement)

        case Loop(line, column, expression, invariant, decreases, statement):

            new_statement = instrument_types(statement)
            return Loop(line, column, expression, invariant, decreases, new_statement)

        case Lock(line, column, lock_id):
            lock_tree_lock_call = LockTreeCall(
                line=line,
                column=column,
                lock_id=lock_id,
                type=LockTreeCallType.LOCK
            )
            return Block(line,column,[program, lock_tree_lock_call])
            
        case Unlock(line, column, lock_id):
            lock_tree_unlock_call = LockTreeCall(
                line=line,
                column=column,
                lock_id=lock_id,
                type=LockTreeCallType.UNLOCK
            )
            return Block(line,column,[program, lock_tree_unlock_call])
        
        case _:
            return program
        
def instrument(program: Node) -> Program:
    if program is None:
        return None
    
    instrumented_program = instrument_types(program)
    
    return instrumented_program
        