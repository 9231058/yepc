# In The Name Of God
# ========================================
# [] File Name : parser.py
#
# [] Creation Date : 31-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
#
# [] Created By : Saman Fekri (samanf74@gmail.com)
# =======================================
import ply.yacc as yacc
from .lex import YEPCLexer
from ..domain.qr import QuadRuple
from ..domain.symtable import SymbolTable
from ..domain.entity import YEPCEntity


class YEPCParser:
    tokens = YEPCLexer.tokens

    precedence = (
        ('left', 'OR_KW', 'ORELSE'),
        ('left', 'AND_KW', 'ANDTHEN'),
        ('left', 'EQ', 'NE'),
        ('left', 'LT', 'GT', 'LE', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'REM'),
        ('left', 'MULT', 'DIV'),
        ('right', 'NOT_KW', 'UMINUS', 'UMULT', 'RANDOM',
         'MINUSMINUS', 'PLUSPLUS'),
        ('nonassoc', 'IFTHEN'),
        ('nonassoc', 'ELSE_KW'),
    )

    def __init__(self):
        self.quadruples = []
        self.symtables = []
        self.offsets = []

    def p_program(self, p):
        'program : programInitiator declarationList'
        self.quadruples.append(QuadRuple(op='goto',
                                         arg1=self.symtables[-1].meta['#aa11']['start'], arg2='', result=''))
        self.printInC()
        print("Rule 1: program -> declarationList")

    def p_program_initiator(self, p):
        'programInitiator : empty'
        print("Rule *: programInitiator -> empty")
        self.symtables.append(SymbolTable(None))
        self.offsets.append(0)

    def p_declaration_list(self, p):
        '''
        declarationList : declarationList declaration
                        | declaration
        '''
        if len(p) == 3:
            print("Rule 2: declarationList -> declarationList declaration")
        else:
            print("Rule 3: declarationList -> declaration")

    def p_declaration_1(self, p):
        '''
        declaration : varDeclaration
        '''
        print("Rule 4: declaration -> varDeclaration")

    def p_declaration_2(self, p):
        '''
        declaration : funDeclaration
        '''
        print("Rule 5: declaration -> funDeclartion")

    def p_declaration_3(self, p):
        '''
        declaration : recDeclaration
        '''
        print("Rule 6: declaration -> recDeclaration")

    def p_rec_declaration(self, p):
        '''
        recDeclaration : RECORD_KW ID BR_OPEN localDeclarations BR_CLOSE
        '''
        print("Rule 7: recDeclaration -> RECORD_KW ID {localDeclarations}")

    def p_var_declaration(self, p):
        '''
        varDeclaration : typeSpecifier varDeclarationList SEMICOLON
        '''
        for (name, value) in p[2]:
            self.symtables[-1].insert_variable(name, p[1])
            self.quadruples.append(QuadRuple(op='', arg1=value, arg2='', result=name))
        print("Rule 8: varDeclaration -> typeSpecifier varDeclarationList;")

    def p_scoped_var_declaration(self, p):
        '''
        scopedVarDeclaration : scopedTypeSpecifier varDeclarationList SEMICOLON
        '''
        for (name, value) in p[2]:
            self.symtables[-1].insert_variable(name, p[1])
            self.quadruples.append(QuadRuple(op='', arg1=value, arg2='', result=name))
        print("Rule 9: scopedVarDeclaration ->",
              "scopedTypeSpecifier varDeclarationList;")

    def p_var_declaration_list(self, p):
        '''
        varDeclarationList : varDeclarationList COMMA varDeclarationInitialize
                           | varDeclarationInitialize
        '''
        if len(p) == 4:
            print("Rule 10: varDeclarationList ->",
                  "varDeclarationList, varDeclarationInitialize")
            p[0] = [*p[1], p[3]]
        else:
            print("Rule 11: varDeclarationList -> varDeclarationInitialize")
            p[0] = [p[1]]

    def p_var_declaration_initialize(self, p):
        '''
        varDeclarationInitialize : varDeclarationId
                                 | varDeclarationId COLON simpleExpression
        '''
        if len(p) == 2:
            print("Rule 12: varDeclarationInitialize -> varDeclarationId")
            p[0] = (p[1], '0')
        else:
            print("Rule 13: varDeclarationInitialize ->",
                  "varDeclarationId: simpleExpression")
            p[0] = (p[1], p[3].place)

    def p_var_declaration_id(self, p):
        '''
        varDeclarationId : ID
                         | ID BK_OPEN NUMCONST BK_CLOSE

        '''
        if len(p) == 2:
            print("Rule 14: varDeclarationId -> ID")
            p[0] = p[1]
        else:
            print("Rule 15: varDeclarationId -> ID [ NUMCONST ]")
            p[0] = '%s[%d]' % (p[1], p[3])

    def p_scoped_type_specifier(self, p):
        '''
        scopedTypeSpecifier : STATIC_KW typeSpecifier
                            | typeSpecifier
        '''
        if len(p) == 3:
            print("Rule 16: scopedTypeSpecifier -> STATIC_KW typeSpecifier")
            p[0] = p[2]
        else:
            print("Rule 17: scopedTypeSpecifier -> typeSpecifier")
            p[0] = p[1]

    def p_type_specifier(self, p):
        '''
        typeSpecifier : returnTypeSpecifier
                      | RECORD_KW ID
        '''
        if len(p) == 2:
            print("Rule 18: typeSpecifier -> returnTypeSpecifier")
            p[0] = p[1]
        else:
            print("Rule 19: typeSpecifier -> RECORD_KW ID")
            p[0] = p[2]

    def p_return_type_specifier_1(self, p):
        '''
        returnTypeSpecifier : INT_T
        '''
        print("Rule 20: returnTypeSpecifier -> INT_T")
        p[0] = 'int'

    def p_return_type_specifier_2(self, p):
        '''
        returnTypeSpecifier : REAL_T
        '''
        print("Rule 21: returnTypeSpecifier -> REAL_T")
        p[0] = 'real'

    def p_return_type_specifier_3(self, p):
        '''
        returnTypeSpecifier : BOOL_T
        '''
        print("Rule 22: returnTypeSpecifier -> BOOL_T")
        p[0] = 'bool'

    def p_return_type_specifier_4(self, p):
        '''
        returnTypeSpecifier : CHAR_T
        '''
        print("Rule 23: returnTypeSpecifier -> CHAR_T")
        p[0] = 'char'

    def p_fun_declaration_1(self, p):
        '''
        funDeclaration :  typeSpecifier ID funInitiator nexter quadder PR_OPEN params PR_CLOSE statement
        '''
        s = self.symtables.pop()
        self.symtables[-1].insert_procedure(p[2], s, p[5].quad, p[7], p[1])
        YEPCEntity.backpatch(p[4].next_list, len(self.quadruples))
        print("Rule 24: funDeclaration -> typeSpecifier ID funInitiator (params) statement")

    def p_fun_declaration_2(self, p):
        '''
        funDeclaration : ID funInitiator nexter quadder PR_OPEN params PR_CLOSE statement
        '''
        s = self.symtables.pop()
        self.symtables[-1].insert_procedure(p[1], s, p[4].quad, p[6], 'void')
        YEPCEntity.backpatch(p[3].next_list, len(self.quadruples))
        print("Rule 25: funDeclaration -> ID funInitiator (params) statement")

    def p_fun_initiator(self, p):
        '''
        funInitiator : empty
        '''
        self.symtables.append(SymbolTable(self.symtables[-1]))
        self.offsets.append(0)

    def p_params_1(self, p):
        '''
        params : paramList
        '''
        p[0] = p[1]
        for (name, type) in p[0]:
            self.quadruples.append(QuadRuple(op='pop', arg1=type, arg2='', result=name))
        print("Rule 26: params -> paramList")

    def p_params_2(self, p):
        '''
        params : empty
        '''
        p[0] = []
        print("Rule 27: params -> empty")

    def p_param_list(self, p):
        '''
        paramList : paramList SEMICOLON paramTypeList
                  | paramTypeList
        '''
        if len(p) == 4:
            p[0] = p[1] + p[3]
            print("Rule 28: paramList -> paramList; paramTypeList")
        else:
            p[0] = p[1]
            print("Rule 29: paramList -> paramTypeList")

    def p_param_type_list(self, p):
        '''
        paramTypeList : typeSpecifier paramIdList
        '''
        p[0] = []
        for name in p[2]:
            p[0].append((name, p[1]))
            self.symtables[-1].insert_variable(name, p[1])
        print("Rule 30: paramTypeList -> typeSpecifier paramIdList")

    def p_param_id_list(self, p):
        '''
        paramIdList : paramIdList COMMA paramId
                    | paramId
        '''
        if len(p) == 4:
            p[0] = [*p[1], p[3]]
            print("Rule 31: paramIdList -> paramIdList , paramId")
        else:
            p[0] = [p[1]]
            print("Rule 32: paramIdList -> paramId")

    def p_param_id(self, p):
        '''
        paramId : ID BK_OPEN BK_CLOSE
                | ID
        '''
        if len(p) == 4:
            p[0] = '%s[]' % p[1]
            print("Rule 33: paramId -> ID [ ]")
        else:
            p[0] = p[1]
            print("Rule 34: paramId -> ID")

    def p_statement_1(self, p):
        '''
        statement : expressionStmt
        '''
        print("Rule 35: statement -> expressionStmt")

    def p_statement_2(self, p):
        '''
        statement : compoundStmt
        '''
        print("Rule 36: statement -> compoundStmt")

    def p_statement_3(self, p):
        '''
        statement : selectionStmt
        '''
        print("Rule 37: statement -> selectionStmt")

    def p_statement_4(self, p):
        '''
        statement : iterationStmt
        '''
        print("Rule 38: statement -> iterationStmt")

    def p_statement_5(self, p):
        '''
        statement : returnStmt
        '''
        print("Rule 39: statement -> returnStmt")

    def p_statement_6(self, p):
        '''
        statement : breakStmt
        '''
        print("Rule 40: statement -> breakStmt")

    def p_compound_stmt(self, p):
        '''
        compoundStmt : BR_OPEN localDeclarations statementList BR_CLOSE
        '''
        print("Rule 41: compoundStmt -> {localDeclarations statementList}")

    def p_local_declarations(self, p):
        '''
        localDeclarations : localDeclarations scopedVarDeclaration
                          | empty
        '''
        if len(p) == 3:
            print("Rule 42: localDeclarations ->",
                  "localDeclarations scopedVarDeclaration")
        else:
            print("Rule 43: localDeclarations ->",
                  "localDeclarations scopedVarDeclaration")

    def p_statement_list(self, p):
        '''
        statementList : statementList statement
                      | empty
        '''
        if len(p) == 3:
            print("Rule 44: statementList -> statementList statement")
        else:
            print("Rule 45: statementList -> empty")

    def p_expression_stmt(self, p):
        '''
        expressionStmt : expression SEMICOLON
                       | SEMICOLON
        '''
        if len(p) == 3:
            print("Rule 46: expressionStmt -> expression;")
        else:
            print("Rule 47: expressionStmt -> ;")

    def p_selection_stmt_1(self, p):
        '''
        selectionStmt : IF_KW PR_OPEN simpleExpression PR_CLOSE quadder statement %prec IFTHEN
        '''
        if (p[3].type == 'bool'):
            YEPCEntity.backpatch(p[3].true_list, p[5].quad)
        print("Rule 48: selectionStmt ->",
              "IF_KW (simpleExpression) statement")

    def p_selection_stmt_2(self, p):
        '''
        selectionStmt : IF_KW PR_OPEN simpleExpression PR_CLOSE quadder statement ELSE_KW quadder statement
        '''
        if (p[3].type == 'bool'):
            YEPCEntity.backpatch(p[3].true_list, p[5].quad)
            YEPCEntity.backpatch(p[3].false_list, p[8].quad)
        print("Rule 49: selectionStmt ->",
              "IF_KW (simpleExpression) statement ELSE_KW statement")

    def p_selection_stmt_3(self, p):
        '''
        selectionStmt : SWITCH_KW PR_OPEN simpleExpression PR_CLOSE caseElement defaultElement END_KW
        '''
        print("Rule 50: selectionStmt ->",
              "SWITCH_KW (simpleExpression) caseElement defaultElement END_KW")

    def p_case_element(self, p):
        '''
        caseElement : CASE_KW NUMCONST COLON statement
                    | caseElement CASE_KW NUMCONST COLON statement
        '''
        if len(p) == 5:
            print("Rule 51: caseElement -> CASE_KW NUMCONST: statement")
        else:
            print("Rule 52: caseElement ->",
                  "caseElement CASE_KW NUMCONST: statement")

    def p_default_element(self, p):
        '''
        defaultElement : DEFAULT_KW COLON statement
                       | empty
        '''
        if len(p) == 4:
            print("Rule 53: defaultElement -> DEFAULT_KW: statement")
        else:
            print("Rule 54: defaultElement -> empty")

    def p_iteration_stmt(self, p):
        '''
        iterationStmt : WHILE_KW PR_OPEN quadder simpleExpression PR_CLOSE quadder statement nexter
        '''
        YEPCEntity.backpatch(p[8].next_list, p[3].quad)
        YEPCEntity.backpatch(p[4].true_list, p[6].quad)
        YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        print("Rule 55: iterationStmt ->",
              "WHILE_KW (simpleExpression) statement")

    def p_return_stmt(self, p):
        '''
        returnStmt : RETURN_KW SEMICOLON
                   | RETURN_KW expression SEMICOLON
        '''
        if len(p) == 3:
            print("Rule 56: returnStmt -> RETURN_KW ;")
        else:
            print("Rule 57: returnStmt -> RETURN_KW expression ;")

    def p_break_stmt(self, p):
        '''
        breakStmt : BREAK_KW SEMICOLON
        '''
        print("Rule 58: breakStmt -> BREAK_KW ;")

    def p_expression_1(self, p):
        '''
        expression : mutable EXP expression
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='', arg1=p[3].place, arg2='',
                                         result=p[1].place))
        print("Rule 59: expression -> mutable EXP expression")

    def p_expression_2(self, p):
        '''
        expression : mutable PLUSEXP expression
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='+', arg1=p[1].place, arg2=p[3].place, result=p[1].place))
        print("Rule 60: expression -> mutable PLUSEXP expression")

    def p_expression_3(self, p):
        '''
        expression : mutable MINUSEXP expression
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='-', arg1=p[1].place, arg2=p[3].place, result=p[1].place))
        print("Rule 61: expression -> mutable MINUSEXP expression")

    def p_expression_4(self, p):
        '''
        expression : mutable MULTEXP expression
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='*', arg1=p[1].place, arg2=p[3].place, result=p[1].place))
        print("Rule 62: expression -> mutable MULTEXP expression")

    def p_expression_5(self, p):
        '''
        expression : mutable DIVEXP expression
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='/', arg1=p[1].place, arg2=p[3].place, result=p[1].place))
        print("Rule 63: expression -> mutable DIVEXP expression")

    def p_expression_6(self, p):
        '''
        expression : simpleExpression
        '''
        p[0] = p[1]
        print("Rule 64: expression -> simpleExpression")

    def p_expression_7(self, p):
        '''
        expression : mutable PLUSPLUS
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='+', arg1=p[1].place, arg2='1', result=p[1].place))
        print("Rule 65: expression -> mutable PLUSPLUS")

    def p_expression_8(self, p):
        '''
        expression : mutable MINUSMINUS
        '''
        p[0] = YEPCEntity()
        p[0].type = p[1].type
        p[0].place = p[1].place
        self.quadruples.append(QuadRuple(op='-', arg1=p[1].place, arg2='1', result=p[1].place))
        print("Rule 66: expression -> mutable MINUSMINUS")

    def p_simple_expression_1(self, p):
        '''
        simpleExpression : simpleExpression OR_KW quadder simpleExpression
        '''
        p[0] = YEPCEntity()
        p[0].type = 'bool'
        t1 = self.symtables[-1].new_temp('int')
        YEPCEntity.backpatch(p[1].true_list, len(self.quadruples))
        self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=t1))
        self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
        YEPCEntity.backpatch(p[1].false_list, len(self.quadruples))
        self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=t1))
        self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))

        p[0].true_list = p[4].true_list
        YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        self.quadruples.append(QuadRuple(op='if', arg1='%s == 0' % t1, arg2='', result=''))
        qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
        p[0].false_list.append(qf)
        self.quadruples.append(qf)
        qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
        p[0].true_list.append(qt)
        self.quadruples.append(qt)
        print("Rule 67: simpleExpression ->",
              "simpleExpression OR_KW simpleExpression")

    def p_simple_expression_2(self, p):
        '''
        simpleExpression : simpleExpression AND_KW quadder simpleExpression
        '''
        p[0] = YEPCEntity()
        p[0].type = 'bool'
        t1 = self.symtables[-1].new_temp('int')
        YEPCEntity.backpatch(p[1].true_list, len(self.quadruples))
        self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=t1))
        self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
        YEPCEntity.backpatch(p[1].false_list, len(self.quadruples))
        self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=t1))
        self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))

        p[0].false_list = p[4].false_list
        YEPCEntity.backpatch(p[4].true_list, len(self.quadruples))
        self.quadruples.append(QuadRuple(op='if', arg1='%s == 0' % t1, arg2='', result=''))
        qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
        p[0].false_list.append(qf)
        self.quadruples.append(qf)
        qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
        p[0].true_list.append(qt)
        self.quadruples.append(qt)

        print("Rule 68: simpleExpression ->",
              "simpleExpression AND_KW simpleExpression")

    def p_simple_expression_3(self, p):
        '''
        simpleExpression : simpleExpression OR_KW ELSE_KW quadder simpleExpression %prec ORELSE
        '''
        p[0] = YEPCEntity()
        p[0].type = 'bool'
        YEPCEntity.backpatch(p[1].false_list, p[4].quad)
        p[0].true_list = p[1].true_list + p[5].true_list
        p[0].false_list = p[5].false_list
        print("Rule 69: simpleExpression ->",
              "simpleExpression OR_KW ELSE_KW simpleExpression")

    def p_simple_expression_4(self, p):
        '''
        simpleExpression : simpleExpression AND_KW THEN_KW quadder simpleExpression %prec ANDTHEN
        '''
        p[0] = YEPCEntity()
        p[0].type = 'bool'
        YEPCEntity.backpatch(p[1].true_list, p[4].quad)
        p[0].false_list = p[1].false_list + p[5].false_list
        p[0].true_list = p[5].true_list
        print("Rule 70: simpleExpression ->",
              "simpleExpression AND_KW THEN_KW simpleExpression")

    def p_simple_expression_5(self, p):
        '''
        simpleExpression : NOT_KW simpleExpression
        '''
        p[0] = YEPCEntity()
        p[0].true_list = p[2].false_list
        p[0].false_list = p[2].true_list
        print("Rule 71: simpleExpression -> NOT_KW simpleExpression")

    def p_simple_expression_6(self, p):
        '''
        simpleExpression : relExpression
        '''
        p[0] = p[1]
        print("Rule 72: simpleExpression -> relExpression")

    def p_quadder(self, p):
        '''
        quadder : empty
        '''
        p[0] = YEPCEntity()
        p[0].quad = len(self.quadruples)
        print("Rule Quadder: quadder -> quadder -> empty")

    def p_nexter(self, p):
        '''
        nexter : empty
        '''
        p[0] = YEPCEntity()
        q = QuadRuple(op='goto', arg1='-', arg2='', result='')
        p[0].next_list.append(q)
        self.quadruples.append(q)

    def p_rel_expression(self, p):
        '''
        relExpression : mathlogicExpression relop mathlogicExpression
                      | mathlogicExpression
        '''
        if len(p) == 4:
            p[0] = YEPCEntity()
            p[0].type = 'bool'
            self.quadruples.append(QuadRuple(op='if', result='',
                                             arg1='%s %s %s' % (p[1].place, p[2], p[3].place),
                                             arg2=''))
            qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
            qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
            p[0].true_list.append(qt)
            p[0].false_list.append(qf)
            self.quadruples.append(qt)
            self.quadruples.append(qf)
            print("Rule 73: relExpression ->",
                  "mathlogicExpression relop mathlogicExpression")
        else:
            p[0] = p[1]
            print("Rule 74: relExpression -> mathlogicExpression")

    def p_relop_1(self, p):
        '''
        relop : LE
        '''
        p[0] = '<='
        print("Rule 75: relop -> LE")

    def p_relop_2(self, p):
        '''
        relop : LT
        '''
        p[0] = '<'
        print("Rule 76: relop -> LT")

    def p_relop_3(self, p):
        '''
        relop : GT
        '''
        p[0] = '>'
        print("Rule 77: relop -> GT")

    def p_relop_4(self, p):
        '''
        relop : GE
        '''
        p[0] = '>='
        print("Rule 78: relop -> GE")

    def p_relop_5(self, p):
        '''
        relop : EQ
        '''
        p[0] = '=='
        print("Rule 79: relop -> EQ")

    def p_relop_6(self, p):
        '''
        relop : NE
        '''
        p[0] = '!='
        print("Rule 80: relop -> NE")

    def p_mathlogic_expression_1(self, p):
        '''
        mathlogicExpression : mathlogicExpression PLUS quadder mathlogicExpression
        '''
        p[0] = YEPCEntity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='+', arg1='1', arg2=p[4].place, result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=p[4].place, arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='+', arg1=p[0].place, arg2='1', result=p[0].place)

                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                self.quadruples.append(QuadRuple(op='+', arg1=p[1].place, arg2=p[4].place,
                                                 result=p[0].place))
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='+', arg1=p[1].place, arg2='1', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=p[1].place, arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples) - 1)
        print("Rule 81: mathlogicExpression ->",
              "mathlogicExpression PLUS mathlogicExpression")

    def p_mathlogic_expression_2(self, p):
        '''
        mathlogicExpression : mathlogicExpression MINUS quadder mathlogicExpression
        '''
        p[0] = YEPCEntity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='-', arg1='1', arg2=p[4].place, result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=p[4].place, arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='-', arg1=p[0].place, arg2='1', result=p[0].place)

                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                self.quadruples.append(QuadRuple(op='-', arg1=p[1].place, arg2=p[4].place,
                                                 result=p[0].place))
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='-', arg1=p[1].place, arg2='1', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=p[1].place, arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples) - 1)
        print("Rule 82: mathlogicExpression ->",
              "mathlogicExpression MINUS mathlogicExpression")

    def p_mathlogic_expression_3(self, p):
        '''
        mathlogicExpression : mathlogicExpression MULT quadder mathlogicExpression
        '''
        p[0] = YEPCEntity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='*', arg1='1', arg2=p[4].place, result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='*', arg1=p[0].place, arg2='1', result=p[0].place)

                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                self.quadruples.append(QuadRuple(op='*', arg1=p[1].place, arg2=p[4].place,
                                                 result=p[0].place))
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='*', arg1=p[1].place, arg2='1', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples) - 1)
        print("Rule 83: mathlogicExpression ->",
              "mathlogicExpression MULT mathlogicExpression")

    def p_mathlogic_expression_4(self, p):
        '''
        mathlogicExpression : mathlogicExpression REM quadder mathlogicExpression
        '''
        p[0] = YEPCEntity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='%', arg1='1', arg2=p[4].place, result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='%', arg1=p[0].place, arg2='1', result=p[0].place)

                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                self.quadruples.append(QuadRuple(op='%', arg1=p[1].place, arg2=p[4].place,
                                                 result=p[0].place))
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='%', arg1=p[1].place, arg2='1', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='%', arg1=p[1].place, arg2='0', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples) - 1)
        print("Rule 84: mathlogicExpression ->",
              "mathlogicExpression REM mathlogicExpression")

    def p_mathlogic_expression_5(self, p):
        '''
        mathlogicExpression : mathlogicExpression DIV quadder mathlogicExpression
        '''
        p[0] = YEPCEntity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='/', arg1='1', arg2=p[4].place, result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='/', arg1=p[0].place, arg2='1', result=p[0].place)

                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                self.quadruples.append(QuadRuple(op='/', arg1=p[1].place, arg2=p[4].place,
                                                 result=p[0].place))
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='/', arg1=p[1].place, arg2='1', result=p[0].place)
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='/', arg1=p[1].place, arg2='0', result=p[0].place)
                self.quadruples.append(q1)
                YEPCEntity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                YEPCEntity.backpatch(p[4].false_list, len(self.quadruples) - 1)
        print("Rule 85: mathlogicExpression ->",
              "mathlogicExpression DIV mathlogicExpression")

    def p_mathlogic_expression_6(self, p):
        '''
        mathlogicExpression : unaryExpression
        '''
        p[0] = p[1]
        print("Rule 86: mathlogicExpression -> unaryExpression")

    def p_unary_expression_1(self, p):
        '''
        unaryExpression : MINUS unaryExpression %prec UMINUS
        '''
        p[0] = YEPCEntity()
        if p[2].type == 'bool':
            p[0].place = self.symtables[-1].new_temp('int')
            p[0].type = 'int'
            q1 = QuadRuple(op='-', arg1='0', arg2='1', result=p[0].place)
            q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
            q3 = QuadRuple(op='=', arg1='0', arg2='', result=p[0].place)
            self.quadruples.append(q1)
            YEPCEntity.backpatch(p[2].true_list, len(self.quadruples) - 1)
            self.quadruples.append(q2)
            self.quadruples.append(q3)
            YEPCEntity.backpatch(p[2].false_list, len(self.quadruples) - 1)
        else:
            p[0].place = self.symtables[-1].new_temp(p[2].type)
            p[0].type = p[2].type
            self.quadruples.append(QuadRuple(op='-', arg1=p[2].place, arg2='',
                                             result=p[0].place))
        print("Rule 87: unraryExpression -> MINUS unaryExpression")

    def p_unary_expression_2(self, p):
        '''
        unaryExpression : RANDOM unaryExpression
        '''
        t = YEPCEntity()
        p[0] = YEPCEntity()
        t.place = self.symtables[-1].new_temp('int')
        t.type = "int"
        self.quadruples.append(QuadRuple(op='rand', arg1='', arg2='',
                                         result=t.place))
        p[0].place = self.symtables[-1].new_temp('int')
        p[0].type = "int"
        self.quadruples.append(QuadRuple(op='%', arg1=t.place, arg2=p[2].place,
                                         result=p[0].place))
        print("Rule 88: unaryExpression -> RANDOM unaryExpression")

    def p_unary_expression_3(self, p):
        '''
        unaryExpression : MULT unaryExpression %prec UMULT
        '''
        p[0] = YEPCEntity()
        p[0].place = self.symtables[-1].new_temp('int')
        p[0].type = "int"
        self.quadruples.append(QuadRuple(op='sizeof', arg1=p[2].place, arg2='', result=p[0].place))
        print("Rule 89: unaryExpression -> MULT unaryExpression")

    def p_unary_expression_4(self, p):
        '''
        unaryExpression : factor
        '''
        p[0] = p[1]
        print("Rule 90: unaryExpression -> factor")

    def p_factor_1(self, p):
        '''
        factor : immutable
        '''
        p[0] = p[1]
        print("Rule 91: factor -> immutable")

    def p_factor_2(self, p):
        '''
        factor : mutable
        '''
        p[0] = p[1]
        print("Rule 92: factor -> mutable")

    def p_mutable(self, p):
        '''
        mutable : ID
                | mutable BK_OPEN expression BK_CLOSE
                | mutable DOT ID
        '''
        p[0] = YEPCEntity()
        if len(p) == 2:
            p[0].place = p[1]
            p[0].type = self.symtables[-1].symbols[p[1]]
            print("Rule 93: mutable -> ID")
        elif len(p) == 5:
            print("Rule 94: mutable -> mutable[expression]")
        else:
            print("Rule 95: mutbale -> mutable.ID")

    def p_immutable_1(self, p):
        '''
        immutable : PR_OPEN expression PR_CLOSE
        '''
        p[0] = p[2]
        print("Rule 96: immutable -> (expression)")

    def p_immutable_2(self, p):
        '''
        immutable : call
        '''
        print("Rule 97: immutable -> call")

    def p_immutable_3(self, p):
        '''
        immutable : constant
        '''
        p[0] = p[1]
        print("Rule 98: immutable -> constant")

    def p_call(self, p):
        '''
        call : ID PR_OPEN args PR_CLOSE
        '''
        p[0] = YEPCEntity()
        p[0].type = self.symtables[0].meta[p[1]]['return_type']
        p[0].place = self.symtables[-1].new_temp(p[0].type)
        for (name, type) in p[3]:
            self.quadruples.append(QuadRuple(op='push', arg1=name, arg2=type, result=''))
        self.quadruples.append(QuadRuple(op='push', arg1=len(self.quadruples), arg2='int', result=''))
        self.quadruples.append(QuadRuple(op='goto',
                                         arg1=self.symtables[0].meta[p[1]]['start'],
                                         arg2='', result=''))
        self.quadruples.append(QuadRuple(op='pop', arg1=p[0].type, arg2='', result=p[0].place))
        print("Rule 99: call -> ID(args)")

    def p_args_1(self, p):
        '''
        args : argList
        '''
        p[0] = p[1]
        print("Rule 100: args -> argList")

    def p_args_2(self, p):
        '''
        args : empty
        '''
        p[0] = []
        print("Rule 101: args -> empty")

    def p_arg_list(self, p):
        '''
        argList : argList COMMA expression
                | expression
        '''
        if len(p) == 4:
            p[0] = p[1].append(p[3].place, self.symtables[-1].symbols[p[3].place])
            print("Rule 102: argList -> argList, expression")
        else:
            p[0] = [(p[1].place, self.symtables[-1].symbols[p[1].place])]
            print("Rule 103: argList -> expression")

    def p_constant_1(self, p):
        '''
        constant : NUMCONST
        '''
        p[0] = YEPCEntity()
        p[0].place = p[1]
        p[0].type = 'int'
        print("Rule 104: constant -> NUMCONST")

    def p_constant_2(self, p):
        '''
        constant : REALCONST
        '''
        p[0] = YEPCEntity()
        p[0].place = p[1]
        p[0].type = 'real'
        print("Rule 105: constant -> REALCONST")

    def p_constant_3(self, p):
        '''
        constant : CHARCONST
        '''
        p[0] = YEPCEntity()
        p[0].place = p[1]
        p[0].type = 'char'
        print("Rule 106: constant -> CHARCONST")

    def p_constant_4(self, p):
        '''
        constant : TRUE
        '''
        p[0] = YEPCEntity()
        p[0].type = 'bool'
        q = QuadRuple(result='', op='goto', arg1='-', arg2='')
        p[0].true_list.append(q)
        self.quadruples.append(q)
        print("Rule 107: constant -> TRUE")

    def p_constant_5(self, p):
        '''
        constant : FALSE
        '''
        p[0] = YEPCEntity()
        p[0].type = 'bool'
        q = QuadRuple(result='', op='goto', arg1='-', arg2='')
        p[0].false_list.append(q)
        self.quadruples.append(q)
        print("Rule 108: constant -> FALSE")

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input: %s" % p)

    # Empty rule
    def p_empty(self, p):
        '''
        empty :
        '''
        pass

    def build(self, **kwargs):
        '''
        build the parser
        '''
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    def printInC(self):
        c_file = open("output.c","w+")
        c_file.write("#include <stdio.h>\n")
        c_file.write("int main(){\n")
        for i in range(len(self.quadruples)):
            entry = self.quadruples[i]
            label = self.makeLabel(i) + ":"
            op = entry.op
            arg1 = entry.arg_one
            arg2 = entry.arg_two
            result = entry.result
            line = label + " "

            if op == 'if':
                line += "if (" + str(arg1) +")"
            elif op == 'goto':
                if arg1 != "-":
                    line += "goto "+ self.makeLabel(arg1) +";"
            elif op == '+':
                line += str(result) + " = " + str(arg1) + " + " + str(arg2)+";"
            elif op == '-':
                line += str(result) + " = " + str(arg1) + " - " + str(arg2)+";"
            elif op == '*':
                line += str(result) + " = " + str(arg1) + " * " + str(arg2)+";"
            elif op == '/':
                line += str(result) + " = " + str(arg1) + " / " + str(arg2)+";"
            elif op == '%':
                line += str(result) + " = " + str(arg1) + " % " + str(arg2)+";"
            #line += str(op) + " " + str(arg1) + " " + str(arg2) + " "+str(result)
            c_file.write(line+"\n")
        c_file.write("}")
        c_file.close()
        print("ouput.c generated")

    def makeLabel(self,index):
        return ("L"+str(index))
