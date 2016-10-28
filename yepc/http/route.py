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

lexer = YEPCLexer()


# About

@app.route('/about')
def about_handler():
        return "18.20 is leaving us"


# UI

@app.route('/<path:path>', methods=['GET'])
def ui_handler(path):
    return flask.send_from_directory('yepc-UI', path)


@app.route('/', methods=['GET'])
def root_handler():
    return flask.send_file('yepc-UI/index.html')


# Lex Phase

@app.route('/lex', methods=['POST'])
def lex_handler():
    data = flask.request.form['text']
    print(data)
    result = []

    l = lexer.build()

    l.input(data)

    for tok in l:
        result.append({
            'type': tok.type,
            'value': tok.value,
            'lineno': tok.lineno,
            'lexpos': tok.lexpos
        })

    return json.dumps(result)
