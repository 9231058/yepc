# In The Name Of God
# ========================================
# [] File Name : yacc.py
#
# [] Creation Date : 31-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
#
# [] Created By : Saman Fekri (samanf74@gmail.com)
# =======================================
import ply.yacc as yacc
from .lex import YEPCLexer


class YEPCParser:
    tokens = YEPCLexer.tokens

    def p_program(self, p):
        'program : declarationList'
        pass

    def p_declaration_list(self, p):
        '''
        declarationList : declarationListDeclaration
                        | declaration
        '''
        pass

    def p_declaration(self, p):
        '''
        declaration : varDeclaration
                    | funDeclaration
                    | recDeclaration
        '''
        pass

    def p_rec_declaration(self, p):
        '''
        recDeclaration : RECORD_KW ID BR_OPEN localDeclaration BR_CLOSE
        '''
        pass

    def p_var_declaration(self, p):
        '''
        varDeclaration : typeSpecifier varDeclarationList SEMICOLON
        '''
        pass

    def p_var_declaration_list(self, p):
        '''
        varDeclarationList : varDeclaraionList COMMA varDeclarationInitialize
                           | varDeclarationInitialize
        '''
        pass

    def p_var_declaration_initialize(self, p):
        '''
        varDeclarationInitialize : varDeclarationId
                                 | varDeclarationId COLON simpleExpression
        '''
        pass

    def p_var_declaration_id(self, p):
        '''
        varDeclarationId : ID
                         | ID BK_OPEN NUMCONST BK_CLOSE

        '''
        pass

    def p_type_specifier(self, p):
        '''
        typeSpecifier : returnTypeSpecifier
                      | ID
        '''
        pass

    def p_return_type_specifier(self, p):
        '''
        returnTypeSpecifier : INT_T
                            | REAL_T
                            | BOOL_T
                            | CHAR_T
        '''
        pass

    def p_fun_declaration(self, p):
        '''
        funDeclaration : typeSpecifier ID PR_OPEN params PR_CLOSE statement
                       | ID PR_OPEN params PR_CLOSE statement
        '''
        pass

    def p_params(self, p):
        '''
        params : paramList
               | empty
        '''
        pass

    def p_param_list(self, p):
        '''
        paramList : paramList SEMICOLON paramTypeList
                  | paramTypeList
        '''
        pass

    def p_param_type_list(self, p):
        '''
        paramTypeList : typeSpecifier paramIdList
        '''
        pass

    def p_param_id_list(self, p):
        '''
        paramIdList : paramIdList COMMA paramId
                    | paramId
        '''
        pass

    def p_param_id(self, p):
        '''
        paramId : ID
                | ID BR_OPEN BR_CLOSE
        '''
        if len(p) == 2:
            print(p[1])
        else:
            print("%s[]" % p[1])

    def p_statement(self, p):
        '''
        statement : expressionStmt
                  | compoundStmt
                  | selectionStmt
                  | iterationStmt
                  | returnStmt
                  | breakStmt
        '''
        pass

    def p_expression(self, p):
        '''
        expression : mutable EXP_OP expression
                   | mutable MATH_OP EXP_OP expression
                   | simpleExpression
                   | mutable MATH_OP MATH_OP
        '''
        pass

    def p_simple_expression(self, p):
        '''
        simpleExpression : simpleExpression OR_KW simpleExpression
                         | simpleExpression AND_KW simpleExpression
                         | simpleExpression OR_KW ELSE_KW simpleExpression
                         | simpleExpression AND_KW THEN_KW simpleExpression
                         | NOT_KW simpleExpression
                         | relExpression
        '''
        pass

    def p_rel_expression(self, p):
        '''
        relExpression : mathlogicExpression REL_OP mathlogicExpression
                      | mathlogicExpression
        '''
        pass

    def p_mathlogic_expression(self, p):
        '''
        mathlogicExpression : mathlogicExpression MATH_OP mathlogicExpression
                            | unaryExpression
        '''
        pass

    def p_unary_expression(self, p):
        '''
        unaryExpression : MATH_OP unaryExpression
                        | factor
        '''
        pass

    def p_factor(self, p):
        '''
        factor : immutable
               | mutable
        '''
        pass

    def p_constant(self, p):
        '''
        constant : NUMCONST
                 | REALCONST
                 | CHARCONST
                 | TRUE
                 | FALSE
        '''
        pass

    def p_arg_list(self, p):
        '''
        argList : argList COMMA expression
                | expression
        '''
        pass

    def p_args(self, p):
        '''
        args : argList
             | empty
        '''
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")

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
