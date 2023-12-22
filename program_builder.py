from antlr4_generated.ProgramParser import ProgramParser
from antlr4_generated.ProgramVisitor import ProgramVisitor
from program.program import Program
from program.function import Function
from program.function_call import FunctionCall
from program.assignment import Assignment
from program.if_else import IfElse
from program.loop import Loop
from program.assertion import Assertion
from program.write import Write
from assignment1.lock_tree.lock_tree_call import LockTreeCall, LockTreeCallType
from program.lock import Lock
from program.unlock import Unlock
from program.literal_int import LiteralInt
from program.literal_bool import LiteralBool
from program.id import Id
from program.parentheses import Parentheses
from program.negate import Negate
from program.negative import Negative
from program.arithmetic import Arithmetic, ArithmeticType
from program.implication import Implication
from program.compare import Compare, CompareType
from program.and_or import AndOr, AndOrType
from program.type import Type
from program.block import Block
from program.list_set import ListSet
from program.list import List
from program.list_get import ListGet
from program.length import Length
from program.forall import Forall
from program.exists import Exists


class ProgramBuilder(ProgramVisitor):
    def visitProgram(self, ctx: ProgramParser.ProgramContext):
        function = self.visit(ctx.function())

        if function is None:
            return None
        
        return Program(
            ctx.start.line, 
            ctx.start.column, 
            function, 
            self.visit(ctx.functionCall()) if ctx.functionCall() is not None else None
        )
    
    def visitFunction(self, ctx: ProgramParser.FunctionContext):
        return Function(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText(),
            self.visit(ctx.functionParameters()) if ctx.functionParameters() is not None else [],
            self.visit(ctx.functionPreCondition().expression()) if ctx.functionPreCondition() is not None else None,
            self.visit(ctx.functionPostCondition().expression()) if ctx.functionPostCondition() is not None else None,
            self.visit(ctx.statement())
        )
    
    def visitFunctionParameters(self, ctx: ProgramParser.FunctionParametersContext):
        return [self.visit(functionParameter) for functionParameter in ctx.functionParameter()]
    
    def visitFunctionParameter(self, ctx: ProgramParser.FunctionParameterContext):
        id = ctx.ID().getText()
        match ctx.TYPE().getText():
            case 'int':
                return id, Type.INT
            case 'bool':
                return id, Type.BOOL
            case 'int[]':
                return id, Type.LIST_INT
    
    def visitFunctionCall(self, ctx: ProgramParser.FunctionCallContext):
        return FunctionCall(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText(),
            self.visit(ctx.functionCallArguments()) if ctx.functionCallArguments() is not None else []
        )
    
    def visitFunctionCallArguments(self, ctx: ProgramParser.FunctionCallArgumentsContext):
        return [self.visit(expression) for expression in ctx.expression()]
    
    def visitAssignmentStatement(self, ctx: ProgramParser.AssignmentStatementContext):
        return Assignment(
            ctx.ID().getSymbol().line,
            ctx.ID().getSymbol().column,
            self.visit(ctx.expression()), ctx.ID().getText()
            )

    def visitBlockStatement(self, ctx:ProgramParser.BlockStatementContext):
        return Block(
            ctx.start.line,
            ctx.start.column,
            [self.visit(statement) for statement in ctx.statement()]
        )
    
    def visitIfElseStatement(self, ctx: ProgramParser.IfElseStatementContext):
        else_statement_ctx = ctx.statement(1)
        return IfElse(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression()), 
            self.visit(ctx.statement(0)),
            self.visit(else_statement_ctx) if else_statement_ctx is not None else None
            )
    
    def visitLoopStatement(self, ctx: ProgramParser.LoopStatementContext):
        return Loop(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression()),
            self.visit(ctx.loopInvariantCondition().expression()) if ctx.loopInvariantCondition() is not None else None,
            [self.visit(expression) for expression in ctx.loopDecreasesConditions().expression()] if ctx.loopDecreasesConditions() is not None else None,
            self.visit(ctx.statement())
            )
    
    def visitAssertionStatement(self, ctx: ProgramParser.AssertionStatementContext):
        return Assertion(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression())
            )
    
    def visitWriteStatement(self, ctx: ProgramParser.WriteStatementContext):
        return Write(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression())
            )
    
    def visitLockStatement(self, ctx: ProgramParser.LockStatementContext):
        return Lock(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText()
        )
    
    def visitUnlockStatement(self, ctx: ProgramParser.UnlockStatementContext):
        return Unlock(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText()
        )

    def visitLockTreeLockStatement(self, ctx: ProgramParser.LockTreeLockStatementContext):
        return LockTreeCall(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText(),
            LockTreeCallType.LOCK
        )

    def visitLockTreeUnlockStatement(self, ctx: ProgramParser.LockTreeUnlockStatementContext):
        return LockTreeCall(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText(),
            LockTreeCallType.UNLOCK
        )

    def visitListSetStatement(self, ctx:ProgramParser.ListSetStatementContext):
        return ListSet(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText(),
            self.visit(ctx.expression(0)),
            self.visit(ctx.expression(1))
        )
    
    def visitLiteralExpression(self, ctx: ProgramParser.LiteralExpressionContext):
        if ctx.LITERAL_INT() is not None:
            return LiteralInt(
                ctx.LITERAL_INT().getSymbol().line,
                ctx.LITERAL_INT().getSymbol().column,
                int(ctx.LITERAL_INT().getText())
                )
        
        return LiteralBool(
            ctx.LITERAL_BOOL().getSymbol().line,
            ctx.LITERAL_BOOL().getSymbol().column,
            True if ctx.LITERAL_BOOL().getText() == 'true' else False
            )
    
    def visitIdExpression(self, ctx: ProgramParser.IdExpressionContext):
        return Id(
            ctx.ID().getSymbol().line,
            ctx.ID().getSymbol().column,
            ctx.ID().getText()
            )
    
    def visitParenthesesExpression(self, ctx: ProgramParser.ParenthesesExpressionContext):
        return Parentheses(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression())
            )
    
    def visitNegateExpression(self, ctx: ProgramParser.NegateExpressionContext):
        return Negate(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression())
            )
    
    def visitNegativeExpression(self, ctx: ProgramParser.NegativeExpressionContext):
        return Negative(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression())
            )
    
    def visitArithmeticExpression(self, ctx: ProgramParser.ArithmeticExpressionContext):
        type = None

        match ctx.operation.type:
            case ProgramParser.ADD: 
                type = ArithmeticType.ADD
            case ProgramParser.SUBTRACT: 
                type = ArithmeticType.SUBTRACT
            case ProgramParser.MULTIPLY: 
                type = ArithmeticType.MULTIPLY
            case ProgramParser.DIVIDE: 
                type = ArithmeticType.DIVIDE

        return Arithmetic(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression(0)), 
            self.visit(ctx.expression(1)), 
            type
            )

    def visitImplicationExpression(self, ctx:ProgramParser.ImplicationExpressionContext):
        return Implication(ctx.start.line, ctx.start.column, self.visit(ctx.expression(0)), self.visit(ctx.expression(1)))

    def visitCompareExpression(self, ctx: ProgramParser.CompareExpressionContext):
        type = None

        match ctx.operation.type:
            case ProgramParser.EQUAL:
                type = CompareType.EQUAL
            case ProgramParser.NOT_EQUAL:
                type = CompareType.NOT_EQUAL
            case ProgramParser.GREATER:
                type = CompareType.GREATER
            case ProgramParser.LESS:
                type = CompareType.LESS
            case ProgramParser.GREATER_EQUAL:
                type = CompareType.GREATER_EQUAL
            case ProgramParser.LESS_EQUAL:
                type = CompareType.LESS_EQUAL

        return Compare(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression(0)), 
            self.visit(ctx.expression(1)), 
            type
            )
    
    def visitAndOrExpression(self, ctx: ProgramParser.AndOrExpressionContext):
        type = None

        match ctx.operation.type:
            case ProgramParser.AND:
                type = AndOrType.AND
            case ProgramParser.OR:
                type = AndOrType.OR

        return AndOr(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression(0)), 
            self.visit(ctx.expression(1)), 
            type
            )

    def visitListExpression(self, ctx:ProgramParser.ListExpressionContext):
        return List(
            ctx.start.line,
            ctx.start.column,
            [self.visit(expression) for expression in ctx.expression()]
        )

    def visitListGetExpression(self, ctx:ProgramParser.ListGetExpressionContext):
        return ListGet(
            ctx.start.line,
            ctx.start.column,
            self.visit(ctx.expression()),
            ctx.ID().getText()
        )

    def visitListLengthExpression(self, ctx:ProgramParser.ListLengthExpressionContext):
        return Length(
            ctx.start.line,
            ctx.start.column,
            ctx.ID().getText()
        )

    def visitForallExpression(self, ctx:ProgramParser.ForallExpressionContext):
        return Forall(ctx.start.line, ctx.start.column, self.visit(ctx.expression()), [id.getText() for id in ctx.ID()])

    def visitExistsExpression(self, ctx:ProgramParser.ExistsExpressionContext):
        return Exists(ctx.start.line, ctx.start.column, self.visit(ctx.expression()), [id.getText() for id in ctx.ID()])
