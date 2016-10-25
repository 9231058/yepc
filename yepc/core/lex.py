# In The Name Of God
# ========================================
# [] File Name : lex.py
#
# [] Creation Date : 23-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
#
# [] Created By : Saman Fekri (samanf74@gmail.com)
# =======================================
import ply.lex as lex


class YEPCLexer:
    tokens = (
        'INT_T', 'BOOL_T', 'REAL_T', 'CHAR_T',
        'IF_KW', 'THEN_KW', 'ELSE_KW', 'SWITCH_KW', 'CASE_KW', 'END_KW',
        'WHILE_KW', 'DEFAULT_KW', 'RETURN_KW', 'BREAK_KW',
        'ID',
        'NUMBER', 'CHARCONST', 'REL_OP', 'MATH_OP', 'EXP_OP',
        'WHITE_SPACE', 'COMMENTS',
    )

    # Tokens
    # Keywords
    t_IF_KW = r'if'
    t_THEN_KW = r'then'
    t_ELSE_KW = r'else'
    t_SWITCH_KW = r'switch'
    t_CASE_KW = r'case'
    t_END_KW = r'end'
    t_WHILE_KW = r'while'
    t_DEFAULT_KW = r'default'
    t_RETURN_KW = r'return'
    t_BREAK_KW = r'break'

    # Comments
    def t_COMMENTS(self, t):
        r'\/\/.*'
        pass

    # Types
    t_INT_T = r'int'
    t_BOOL_T = r'bool'
    t_REAL_T = r'real'
    t_CHAR_T = r'char'

    # Operators
    t_REL_OP = r'\.eq | \.gt | \.ge | \.lt | \.le'
    t_MATH_OP = r'\+ | \- | \* | \/'
    t_EXP_OP = r'= | \+= | \-= | \*= | \/= | \+\+ | \-\-'

    # etc
    t_ID = r'\#[a-zA-Z]{2}[0-9]{2}'
    t_WHITE_SPACE = r'[ \t\n]+'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
            return t

    def t_CHARCONST(self, t):
        r"'\\?\w'"
        try:
            if len(t.value) == 4:
                if t.value == "'\\n'":
                    print('new line')
                elif t.value == "'\\0'":
                    print('null')
                else:
                    t.value = str(t.value[2])
            else:
                t.value = str(t.value[1])
        except ValueError:
            print("Character Value error %s", t.value)
        return t

    # Ignored characters
    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value)
        t.lexer.skip(1)

    def build(self, **kwargs):
        '''
        build the lexer
        '''
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
