import unittest
from semantic_analysis import build_parse_tree, build_program, check as checkProgram
from program.program import Program
from program.type import Type
from pathlib import Path
from assignment2.verification import verify
from assignment2.errors.function_verification_error import FunctionVerificationError
from assignment2.errors.invariant_verification_error import InvariantVerificationError, InvariantVerificationErrorType
from assignment2.errors.termination_verification_error import TerminationVerificationError, TerminationVerificationErrorType

Variables = dict[str, Type]
Errors = list[str]


class Test(unittest.TestCase):
    def __build_program(self, file_path: str) -> tuple[Program, Variables, Errors] | None:
        parse_tree = build_parse_tree(str(Path(__file__).parent.joinpath(file_path).resolve()))
        program = build_program(parse_tree)
        program_meta_data = checkProgram(program)

        if program_meta_data is None:
            return None

        variables, variables_expressions, errors = program_meta_data

        return program, variables, errors

    def test_1(self):
        program, variables, errors = self.__build_program('test_1.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 1)
        self.assertIn(FunctionVerificationError('test1', 1, 0), errors)


    def test_2(self):
        program, variables, errors = self.__build_program('test_2.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 3)
        self.assertIn(FunctionVerificationError('test2', 1, 0), errors)
        self.assertIn(InvariantVerificationError(6, 4, InvariantVerificationErrorType.NOT_AN_INVARIANT), errors)
        self.assertIn(InvariantVerificationError(6, 4, InvariantVerificationErrorType.POSTCONDITION_MISMATCH), errors)


    def test_3(self):
        program, variables, errors = self.__build_program('test_3.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 2)
        self.assertIn(FunctionVerificationError('test3', 1, 0), errors)
        self.assertIn(InvariantVerificationError(5, 4, InvariantVerificationErrorType.NOT_AN_INVARIANT), errors)


    def test_4(self):
        program, variables, errors = self.__build_program('test_4.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 2)
        self.assertIn(FunctionVerificationError('test4', 1, 0), errors)
        self.assertIn(InvariantVerificationError(5, 4, InvariantVerificationErrorType.POSTCONDITION_MISMATCH), errors)

    def test_5(self):
        program, variables, errors = self.__build_program('test_5.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 3)
        self.assertIn(FunctionVerificationError('test5', 1, 0), errors)
        self.assertIn(TerminationVerificationError(6, 4, TerminationVerificationErrorType.NOT_BOUNDED), errors)
        self.assertIn(TerminationVerificationError(6, 4, TerminationVerificationErrorType.INVALID), errors)

    def test_6(self):
        program, variables, errors = self.__build_program('test_6.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 2)
        self.assertIn(FunctionVerificationError('test6', 1, 0), errors)
        self.assertIn(TerminationVerificationError(6, 4, TerminationVerificationErrorType.NOT_BOUNDED), errors)
        

    def test_7(self):
        program, variables, errors = self.__build_program('test_7.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 2)
        self.assertIn(FunctionVerificationError('test7', 1, 0), errors)
        self.assertIn(TerminationVerificationError(5, 4, TerminationVerificationErrorType.INVALID), errors)

    def test_8(self):
        program, variables, errors = self.__build_program('test_8.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 1)
        self.assertIn(FunctionVerificationError('test8', 1, 0), errors)

    def test_9(self):
        program, variables, errors = self.__build_program('test_9.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 2)
        self.assertIn(FunctionVerificationError('test9', 1, 0), errors)
        self.assertIn(InvariantVerificationError(5, 4, InvariantVerificationErrorType.NOT_AN_INVARIANT), errors)

    def test_10(self):
        program, variables, errors = self.__build_program('test_10.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)
    
    def test_11(self):
        program, variables, errors = self.__build_program('test_11.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_12(self):
        program, variables, errors = self.__build_program('test_12.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 1)

    def test_13(self):
        program, variables, errors = self.__build_program('test_13.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 1)

    def test_14(self):
        program, variables, errors = self.__build_program('test_14.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 1)

    def test_15(self):
        program, variables, errors = self.__build_program('test_15.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_16(self):
        program, variables, errors = self.__build_program('test_16.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 2)
        self.assertIn(FunctionVerificationError('test16', 1, 0), errors)
        self.assertIn(InvariantVerificationError(5, 4, InvariantVerificationErrorType.NOT_AN_INVARIANT), errors)

    def test_17(self):
        program, variables, errors = self.__build_program('test_17.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 4)
        self.assertIn(FunctionVerificationError('test17', 1, 0), errors)
        self.assertIn(InvariantVerificationError(5, 4, InvariantVerificationErrorType.POSTCONDITION_MISMATCH), errors)
        self.assertIn(InvariantVerificationError(5, 4, InvariantVerificationErrorType.NOT_AN_INVARIANT), errors)
        self.assertIn(InvariantVerificationError(8, 8, InvariantVerificationErrorType.NOT_AN_INVARIANT), errors)
    
    def test_18(self):
        program, variables, errors = self.__build_program('test_18.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_19(self):
        program, variables, errors = self.__build_program('test_19.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 1)
        self.assertIn(FunctionVerificationError('test19', 1, 0), errors)

    def test_20(self):
        program, variables, errors = self.__build_program('test_20.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_21(self):
        program, variables, errors = self.__build_program('test_21.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_22(self):
        program, variables, errors = self.__build_program('test_22.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_23(self):
        program, variables, errors = self.__build_program('test_23.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)

    def test_24(self):
        program, variables, errors = self.__build_program('test_24.txt')
        errors = []
        verify(program, variables, errors)
        self.assertEqual(len(errors), 0)