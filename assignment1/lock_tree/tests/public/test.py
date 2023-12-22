import unittest
from program.loop import Loop
from semantic_analysis import build_parse_tree, build_program, check as checkProgram
from program.program import Program
from pathlib import Path
from assignment1.lock_tree.checking import interpret, interpret_statement_callback
from assignment1.lock_tree.algorithm import build_lock_tree, check
from program.expression import Expression
from assignment1.lock_tree.warnings.deadlock_warning import DeadlockWarning
from program.lock import Lock
from program.unlock import Unlock
from assignment1.instrumentation import instrument
from assignment1.lock_tree.lock_tree_call import LockTreeCall, LockTreeCallType
from assignment1.lock_tree.warnings.double_locking_warning import DoubleLockingWarning
from assignment1.lock_tree.warnings.invalid_locking_pattern_warning import InvalidLockingPatternWarning
from assignment1.lock_tree.warnings.invalid_unlocking_warning import InvalidUnlockingWarning

VariablesExpressions = dict[str, Expression]
Errors = list[str]


class Test(unittest.TestCase):
    def __build_program(self, file_path: str) -> tuple[Program, VariablesExpressions, Errors] | None:
        parse_tree = build_parse_tree(str(Path(__file__).parent.joinpath(file_path).resolve()))
        program = build_program(parse_tree)
        program_meta_data = checkProgram(program)

        if program_meta_data is None:
            return None

        variables, variables_expressions, errors = program_meta_data

        if variables_expressions is None:
            return None

        return program, variables_expressions, errors

    def __build_lock_tree_calls(self, thread_id: str, program: Program, variables_expressions: VariablesExpressions, errors: Errors):
        lock_tree_calls = []
        interpret(
            program,
            variables_expressions,
            errors,
            lambda statement: interpret_statement_callback(statement, lock_tree_calls)
        )
        return (thread_id, lock_tree_calls)

    def test_construction_1(self):
        program, variables_expressions, errors = self.__build_program('test_construction_1.txt')
        lock_tree_calls = self.__build_lock_tree_calls('thread-1', program, variables_expressions, errors)
        warnings = []
        lock_tree = build_lock_tree(lock_tree_calls, warnings)
        self.assertEqual(len(warnings), 0)
        self.assertEqual(len(lock_tree.children), 1)
        self.assertEqual(lock_tree.children[0].lock_id, 'l1')

    def test_construction_2(self):
        program, variables_expressions, errors = self.__build_program('test_construction_2.txt')
        lock_tree_calls = self.__build_lock_tree_calls('thread-1', program, variables_expressions, errors)
        warnings = []
        lock_tree = build_lock_tree(lock_tree_calls, warnings)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], DoubleLockingWarning)
        self.assertEqual(warnings[0].lock_pattern[0][0], 'l1')
        self.assertEqual(warnings[0].lock_pattern[0][1], 3)
        self.assertEqual(warnings[0].lock_pattern[0][2], 4)
        self.assertEqual(warnings[0].lock_pattern[1][0], 'l1')
        self.assertEqual(warnings[0].lock_pattern[1][1], 2)
        self.assertEqual(warnings[0].lock_pattern[1][2], 4)

    def test_construction_3(self):
        program, variables_expressions, errors = self.__build_program('test_construction_3.txt')
        lock_tree_calls = self.__build_lock_tree_calls('thread-1', program, variables_expressions, errors)
        warnings = []
        lock_tree = build_lock_tree(lock_tree_calls, warnings)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], InvalidLockingPatternWarning)
        self.assertEqual(warnings[0].lock_pattern[0][0], 'l1')
        self.assertEqual(warnings[0].lock_pattern[0][1], 4)
        self.assertEqual(warnings[0].lock_pattern[0][2], 4)
        self.assertEqual(warnings[0].lock_pattern[1][0], 'l2')
        self.assertEqual(warnings[0].lock_pattern[1][1], 3)
        self.assertEqual(warnings[0].lock_pattern[1][2], 4)

    def test_construction_4(self):
        program, variables_expressions, errors = self.__build_program('test_construction_4.txt')
        lock_tree_calls = self.__build_lock_tree_calls('thread-1', program, variables_expressions, errors)
        warnings = []
        lock_tree = build_lock_tree(lock_tree_calls, warnings)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], InvalidUnlockingWarning)
        self.assertEqual(warnings[0].lock[0], 'l1')
        self.assertEqual(warnings[0].lock[1], 2)
        self.assertEqual(warnings[0].lock[2], 4)

    def test_deadlock_detection_1(self):
        programs_data = [self.__build_program(file_path) for file_path in [
            'test_deadlock_detection_1_1.txt',
            'test_deadlock_detection_1_2.txt'
        ]]

        programs_lock_tree_calls = [self.__build_lock_tree_calls('thread-' + str(i + 1), programs_data[i][0], programs_data[i][1], programs_data[i][2]) for i in range(len(programs_data))]
        warnings = []
        check(programs_lock_tree_calls, warnings)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], DeadlockWarning)
        self.assertIn(('thread-1', (('l1', 2, 2), ('l2', 3, 2))), warnings[0].deadlock_information)
        self.assertIn(('thread-2', (('l2', 3, 6), ('l1', 4, 6))), warnings[0].deadlock_information)
    
    def test_deadlock_detection_2(self):
        programs_data = [self.__build_program(file_path) for file_path in [
            'test_deadlock_detection_2_1.txt',
            'test_deadlock_detection_2_2.txt'
        ]]

        programs_lock_tree_calls = [self.__build_lock_tree_calls('thread-' + str(i + 1), programs_data[i][0], programs_data[i][1], programs_data[i][2]) for i in range(len(programs_data))]
        warnings = []
        check(programs_lock_tree_calls, warnings)

        self.assertEqual(len(warnings), 4)
        self.assertIsInstance(warnings[0], DeadlockWarning)
        self.assertIsInstance(warnings[1], DeadlockWarning)
        self.assertIsInstance(warnings[2], DeadlockWarning)
        self.assertIsInstance(warnings[3], DeadlockWarning)
        self.assertIn(('thread-1', (('l2', 3, 2), ('l4', 6, 2))), warnings[0].deadlock_information)
        self.assertIn(('thread-2', (('l4', 3, 6), ('l2', 5, 6))), warnings[0].deadlock_information)
        
        self.assertIn(('thread-1', (('l5', 10, 2), ('l8', 11, 2))), warnings[1].deadlock_information)
        self.assertIn(('thread-2', (('l8', 4, 6), ('l5', 7, 6))), warnings[1].deadlock_information)

        self.assertIn(('thread-1', (('l16', 14, 2), ('l13', 16, 2))), warnings[2].deadlock_information)
        self.assertIn(('thread-2', (('l13', 13, 6), ('l16', 17, 6))), warnings[2].deadlock_information)
        
        self.assertIn(('thread-1', (('l15', 15, 2), ('l13', 16, 2))), warnings[3].deadlock_information)
        self.assertIn(('thread-2', (('l13', 13, 6), ('l15', 15, 6))), warnings[3].deadlock_information)

    def test_deadlock_detection_3(self):
        programs_data = [self.__build_program(file_path) for file_path in [
            'test_deadlock_detection_3_1.txt',
            'test_deadlock_detection_3_2.txt'
        ]]

        programs_lock_tree_calls = [self.__build_lock_tree_calls('thread-' + str(i + 1), programs_data[i][0], programs_data[i][1], programs_data[i][2]) for i in range(len(programs_data))]
        warnings = []
        check(programs_lock_tree_calls, warnings)

        self.assertEqual(len(warnings), 0)

    def test_deadlock_detection_4(self):
        programs_data = [self.__build_program(file_path) for file_path in [
            'test_deadlock_detection_4_1.txt',
            'test_deadlock_detection_4_2.txt'
        ]]

        programs_lock_tree_calls = [self.__build_lock_tree_calls('thread-' + str(i + 1), programs_data[i][0], programs_data[i][1], programs_data[i][2]) for i in range(len(programs_data))]
        warnings = []
        check(programs_lock_tree_calls, warnings)

        self.assertEqual(len(warnings), 1)
        self.assertIn(('thread-1', (('l1', 2, 2), ('l2', 5, 2))), warnings[0].deadlock_information)
        self.assertIn(('thread-2', (('l2', 3, 6), ('l1', 4, 6))), warnings[0].deadlock_information)

    def test_deadlock_detection_5(self):
        #Existing Gate Lock Test
        programs_data = [self.__build_program(file_path) for file_path in [
            'test_deadlock_detection_5_1.txt',
            'test_deadlock_detection_5_2.txt'
        ]]

        programs_lock_tree_calls = [self.__build_lock_tree_calls('thread-' + str(i + 1), programs_data[i][0], programs_data[i][1], programs_data[i][2]) for i in range(len(programs_data))]
        warnings = []
        check(programs_lock_tree_calls, warnings)

        self.assertEqual(len(warnings), 0)

    def test_deadlock_detection_6(self):
        programs_data = [self.__build_program(file_path) for file_path in [
            'test_deadlock_detection_6_1.txt',
            'test_deadlock_detection_6_2.txt'
        ]]

        programs_lock_tree_calls = [self.__build_lock_tree_calls('thread-' + str(i + 1), programs_data[i][0], programs_data[i][1], programs_data[i][2]) for i in range(len(programs_data))]
        warnings = []
        check(programs_lock_tree_calls, warnings)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], DeadlockWarning)
        self.assertIn(('thread-1', (('l3', 3, 2), ('l4', 6, 2))), warnings[0].deadlock_information)
        self.assertIn(('thread-2', (('l4', 9, 6), ('l3', 10, 6))), warnings[0].deadlock_information)

    def test_instrumentation_1(self):
        program, variables_expressions, errors = self.__build_program('test_instrumentation_1.txt')

        self.assertIsInstance(program.function.statement.statements[0], Lock)
        self.assertIsInstance(program.function.statement.statements[1], Unlock)

        program = instrument(program)

        self.assertIsInstance(program.function.statement.statements[0].statements[0], Lock)
        self.assertIsInstance(program.function.statement.statements[0].statements[1], LockTreeCall)
        self.assertEqual(program.function.statement.statements[0].statements[1].type, LockTreeCallType.LOCK)

        self.assertIsInstance(program.function.statement.statements[1].statements[0], Unlock)
        self.assertIsInstance(program.function.statement.statements[1].statements[1], LockTreeCall)
        self.assertEqual(program.function.statement.statements[1].statements[1].type, LockTreeCallType.UNLOCK)

    def test_instrumentation_2(self):
        program, variables_expressions, errors = self.__build_program('test_instrumentation_2.txt')

        self.assertIsInstance(program.function.statement.statements[1], Lock)
        self.assertIsInstance(program.function.statement.statements[2], Unlock)

        program = instrument(program)

        self.assertIsInstance(program.function.statement.statements[3], Loop)
        self.assertIsInstance(program.function.statement.statements[3].statement.statements[0].statements[0], Lock)
        self.assertIsInstance(program.function.statement.statements[3].statement.statements[0].statements[1], LockTreeCall)
        self.assertEqual(program.function.statement.statements[3].statement.statements[0].statements[1].type, LockTreeCallType.LOCK)

        self.assertIsInstance(program.function.statement.statements[3], Loop)
        self.assertIsInstance(program.function.statement.statements[3].statement.statements[2].statements[0], Unlock)
        self.assertIsInstance(program.function.statement.statements[3].statement.statements[2].statements[1], LockTreeCall)
        self.assertEqual(program.function.statement.statements[3].statement.statements[2].statements[1].type, LockTreeCallType.UNLOCK)