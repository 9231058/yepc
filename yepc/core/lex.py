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

tokens = (
    'INT_T', 'BOOL_T', 'REAL_T', 'CHAR_T',
    'IF_KW', 'THEN_KW', 'ELSE_KW', 'SWITCH_KW', 'CASE_KW', 'END_KW',
    'WHILE_KW', 'DEFAULT_KW', 'RETURN_KW', 'BREAK_KW',
    'ID',
    'NUMBER', 'CHARCONST', 'REL_OP', 'MATH_OP',
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

# Types
t_INT_T = r'int'
t_BOOL_T = r'bool'
t_REAL_T = r'real'
t_CHAR_T = r'char'

# Operators
t_REL_OP = r'\.eq | \.gt | \.ge | \.lt | \.le'
t_MATH_OP = r'\+ | \- | \* | \/(?:[^\/])'

# etc
t_ID = r'\#[a-zA-Z]{2}[0-9]{2}'
t_WHITE_SPACE = r'[ \t\n]+'
t_COMMENTS = r'\/\/.*'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
        return t


def t_CHARCONST(t):
    r'\?\c'
    try:
        if t.value == '\n':
            print("new line")
        elif t.value == '\0':
            print("null")
        else:
            t.value = str(t.value)
    except ValueError:
        print("Character Value error %c", t.value)
        return t

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
int #zz99
//It's a fucking comment :)
#zz99 = 1 + 2
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
