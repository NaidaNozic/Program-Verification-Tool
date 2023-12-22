# Generated from Program.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ProgramParser import ProgramParser
else:
    from ProgramParser import ProgramParser

# This class defines a complete generic visitor for a parse tree produced by ProgramParser.

class ProgramVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ProgramParser#program.
    def visitProgram(self, ctx:ProgramParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#function.
    def visitFunction(self, ctx:ProgramParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#functionPreCondition.
    def visitFunctionPreCondition(self, ctx:ProgramParser.FunctionPreConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#functionPostCondition.
    def visitFunctionPostCondition(self, ctx:ProgramParser.FunctionPostConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#functionParameters.
    def visitFunctionParameters(self, ctx:ProgramParser.FunctionParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#functionParameter.
    def visitFunctionParameter(self, ctx:ProgramParser.FunctionParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#functionCall.
    def visitFunctionCall(self, ctx:ProgramParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#functionCallArguments.
    def visitFunctionCallArguments(self, ctx:ProgramParser.FunctionCallArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:ProgramParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#BlockStatement.
    def visitBlockStatement(self, ctx:ProgramParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:ProgramParser.IfElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#LoopStatement.
    def visitLoopStatement(self, ctx:ProgramParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#AssertionStatement.
    def visitAssertionStatement(self, ctx:ProgramParser.AssertionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#WriteStatement.
    def visitWriteStatement(self, ctx:ProgramParser.WriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#LockTreeLockStatement.
    def visitLockTreeLockStatement(self, ctx:ProgramParser.LockTreeLockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#LockTreeUnlockStatement.
    def visitLockTreeUnlockStatement(self, ctx:ProgramParser.LockTreeUnlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#LockStatement.
    def visitLockStatement(self, ctx:ProgramParser.LockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#UnlockStatement.
    def visitUnlockStatement(self, ctx:ProgramParser.UnlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ListSetStatement.
    def visitListSetStatement(self, ctx:ProgramParser.ListSetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#loopInvariantCondition.
    def visitLoopInvariantCondition(self, ctx:ProgramParser.LoopInvariantConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#loopDecreasesConditions.
    def visitLoopDecreasesConditions(self, ctx:ProgramParser.LoopDecreasesConditionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#LiteralExpression.
    def visitLiteralExpression(self, ctx:ProgramParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ListExpression.
    def visitListExpression(self, ctx:ProgramParser.ListExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ArithmeticExpression.
    def visitArithmeticExpression(self, ctx:ProgramParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#CompareExpression.
    def visitCompareExpression(self, ctx:ProgramParser.CompareExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ParenthesesExpression.
    def visitParenthesesExpression(self, ctx:ProgramParser.ParenthesesExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#NegateExpression.
    def visitNegateExpression(self, ctx:ProgramParser.NegateExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ExistsExpression.
    def visitExistsExpression(self, ctx:ProgramParser.ExistsExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#IdExpression.
    def visitIdExpression(self, ctx:ProgramParser.IdExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ForallExpression.
    def visitForallExpression(self, ctx:ProgramParser.ForallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ImplicationExpression.
    def visitImplicationExpression(self, ctx:ProgramParser.ImplicationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ListLengthExpression.
    def visitListLengthExpression(self, ctx:ProgramParser.ListLengthExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#AndOrExpression.
    def visitAndOrExpression(self, ctx:ProgramParser.AndOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#ListGetExpression.
    def visitListGetExpression(self, ctx:ProgramParser.ListGetExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ProgramParser#NegativeExpression.
    def visitNegativeExpression(self, ctx:ProgramParser.NegativeExpressionContext):
        return self.visitChildren(ctx)



del ProgramParser