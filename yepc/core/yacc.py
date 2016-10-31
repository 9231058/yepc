# In The Name Of God
# ========================================
# [] File Name : yacc.py
#
# [] Creation Date : 31-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import ply.yacc as yacc
from .lex import YEPCLexer


class YEPCParser:
    tokens = YEPCLexer.tokens

    def p_param_id(self, p):
        '''paramId : ID
                   | ID BR_OPEN BR_CLOSE
        '''
        if len(p) == 2:
            print(p[1])
        else:
            print("%s[]" % p[1])

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")

    def build(self, **kwargs):
        '''
        build the parser
        '''
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
