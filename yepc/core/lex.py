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
        'WHILE_KW', 'DEFAULT_KW', 'RETURN_KW', 'BREAK_KW', 'RECORD_KW',
        'STATIC_KW', 'NOT_KW', 'AND_KW', 'OR_KW',
        'ID', 'FAKE_ID',
        'NUMCONST', 'CHARCONST', 'REALCONST',
        'LE', 'LT', 'GT', 'GE', 'EQ', 'NE',
        'PLUS', 'MINUS', 'MULT', 'REM', 'DIV', 'RANDOM',
        'PLUSPLUS', 'MINUSMINUS',
        'EXP', 'PLUSEXP', 'MINUSEXP', 'MULTEXP', 'DIVEXP',
        'COMMENTS',
        'TRUE', 'FALSE',
        'SEMICOLON', 'COLON', 'DOT', 'COMMA',
        'BR_OPEN', 'BR_CLOSE', 'PR_OPEN', 'PR_CLOSE', 'BK_OPEN', 'BK_CLOSE',
    )

    # Tokens
    # Keywords
    t_RECORD_KW = r'record'
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
    t_STATIC_KW = r'static'
    t_NOT_KW = r'not'
    t_AND_KW = r'and'
    t_OR_KW = r'or'

    # Boolean
    t_TRUE = r'true'
    t_FALSE = r'false'

    # Punctuation
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_DOT = r'\.'
    t_COMMA = r','

    # Pranthesis and Barcket
    t_BR_OPEN = r'\{'
    t_BR_CLOSE = r'\}'
    t_PR_OPEN = r'\('
    t_PR_CLOSE = r'\)'
    t_BK_OPEN = r'\['
    t_BK_CLOSE = r'\]'

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
    t_EQ = r'\.eq'
    t_GT = r'\.gt'
    t_GE = r'\.ge'
    t_LT = '\.lt'
    t_LE = '\.le'
    t_NE = '\.ne'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULT = r'\*'
    t_DIV = r'\/'
    t_REM = r'%'
    t_RANDOM = r'\?'
    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'
    t_EXP = r'='
    t_PLUSEXP = r'\+='
    t_MINUSEXP = r'\-='
    t_MULTEXP = r'\*='
    t_DIVEXP = r'\/='

    # etc
    t_ID = r'\#[a-zA-Z]{2}[0-9]{2}'
    t_FAKE_ID = r'\#[a-zA-Z]{2}[0-9]{2}[\w]+'

    t_CHARCONST = r"'\\?[\w'\\]'"

    def t_REALCONST(self, t):
        r'\d*\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        return t

    def t_NUMCONST(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    # Ignored characters
    t_ignore = ' \t\r\f\v'

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
