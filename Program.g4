grammar Program ;

program : function functionCall? EOF ;

function : FUNCTION ID '(' functionParameters? ')' functionPreCondition? functionPostCondition? statement ;
functionPreCondition : PRECONDITION expression ;
functionPostCondition : POSTCONDITION expression ;
functionParameters : functionParameter (',' functionParameter)* ;
functionParameter : TYPE ID ;

functionCall : ID '(' functionCallArguments? ')' ';' ;
functionCallArguments : expression (',' expression)* ;

statement : <assoc=right>ID ASSIGN expression ';'                                                   # AssignmentStatement
            | '{' statement+ '}'                                                                    # BlockStatement
            | IF '(' expression ')' statement (ELSE statement)?                                     # IfElseStatement
            | WHILE '(' expression ')' loopInvariantCondition? loopDecreasesConditions? statement   # LoopStatement
            | ASSERT '(' expression ')' ';'                                                         # AssertionStatement
            | WRITE '(' expression ')' ';'                                                          # WriteStatement
            | LOCK_TREE_LOCK '(' ID ')' ';'                                                         # LockTreeLockStatement
            | LOCK_TREE_UNLOCK '(' ID ')'';'                                                        # LockTreeUnlockStatement
            | ID '.' LOCK ';'                                                                       # LockStatement
            | ID '.' UNLOCK ';'                                                                     # UnlockStatement
            | ID '[' expression ']' ASSIGN expression ';'                                           # ListSetStatement
            ;

loopInvariantCondition : INVARIANT expression ;
loopDecreasesConditions : DECREASES expression (',' expression)* ;

expression : (LITERAL_INT | LITERAL_BOOL)                                                                           # LiteralExpression
             | ID                                                                                                   # IdExpression
             | '(' expression ')'                                                                                   # ParenthesesExpression
             | NEGATE expression                                                                                    # NegateExpression
             | SUBTRACT expression                                                                                  # NegativeExpression
             | expression operation=(ADD | SUBTRACT | MULTIPLY | DIVIDE) expression                                 # ArithmeticExpression
             | expression operation=(EQUAL | NOT_EQUAL | GREATER | LESS | GREATER_EQUAL | LESS_EQUAL) expression    # CompareExpression
             | expression operation=(AND | OR) expression                                                           # AndOrExpression
             | expression IMPLIES expression                                                                        # ImplicationExpression
             | '[' (expression (',' expression)*)? ']'                                                              # ListExpression
             | ID '[' expression ']'                                                                                # ListGetExpression
             | ID '.' LENGTH                                                                                        # ListLengthExpression
             | FORALL ID (',' ID)* ':' expression                                                                   # ForallExpression
             | EXISTS ID (',' ID)* ':' expression                                                                   # ExistsExpression
             ;

FUNCTION : 'function' ;
PRECONDITION : 'precondition' ;
POSTCONDITION : 'postcondition' ;
INVARIANT : 'invariant' ;
DECREASES : 'decreases' ;
ASSIGN : '=' ;
IF : 'if' ;
ELSE : 'else' ;
WHILE : 'while' ;
ASSERT : 'assert' ;
WRITE : 'write' ;
LOCK_TREE_LOCK : 'lockTreeLock' ;
LOCK_TREE_UNLOCK : 'lockTreeUnlock' ;
LOCK : 'lock' ;
UNLOCK : 'unlock' ;
LENGTH : 'length' ;
FORALL : 'forall' ;
EXISTS : 'exists' ;

NEGATE : '!' ;
AND : '&&' ;
OR : '||' ;
IMPLIES : '==>' ;

ADD : '+' ;
SUBTRACT : '-' ;
MULTIPLY : '*' ;
DIVIDE : '/' ;

EQUAL : '==' ;
NOT_EQUAL : '!=' ;
GREATER : '>' ;
LESS : '<' ;
GREATER_EQUAL : '>=' ;
LESS_EQUAL : '<=' ;

LITERAL_INT : '0' | ([1-9]+ [0-9]*) ;
LITERAL_BOOL : 'true' | 'false' ;
TYPE : 'int' | 'bool' | 'int[]';
ID : [A-Za-z0-9]+ ;

WHITE_SPACE : [\t \r\n] -> skip ;
COMMENT : '//' ~[\n]* -> skip ;