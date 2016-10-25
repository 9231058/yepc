# In The Name Of God
# ========================================
# [] File Name : route.py
#
# [] Creation Date : 26-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import flask
import json

from . import app
from ..core.lex import YEPCLexer

lexer = YEPCLexer().build()


@app.route('/about')
def about_handler():
        return "18.20 is leaving us"


@app.route('/lex', methods=['POST'])
def lex_handler():
    print(flask.request.data)
    data = flask.request.form['text']
    result = []

    lexer.input(data)

    if lexer.token() is None:
        return json.dumps(result)

    for tok in lexer:
        result.append({
            'type': tok.type,
            'value': tok.value,
            'lineno': tok.lineno,
            'lexpos': tok.lexpos
        })

    return json.dumps(result)
