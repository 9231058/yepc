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
import tarfile
import time

from . import app
from ..core.lex import YEPCLexer
from ..core.parser import YEPCParser
from ..core.to_c import YEPCToC
from ..domain.symtable import SymbolTable

lexer = YEPCLexer()


# About


@app.route("/about")
def about_handler():
    return "18.20 is leaving us"


# UI


@app.route("/<path:path>", methods=["GET"])
def ui_handler(path):
    return flask.send_file("yepc-UI/dist/" + path)


@app.route("/", methods=["GET"])
def root_handler():
    return flask.send_file("yepc-UI/dist/index.html")


# Lex Phase


@app.route("/lex", methods=["POST"])
def lex_handler():
    data = flask.request.data.decode("ASCII")

    result = []

    l = lexer.build()

    l.input(data)

    for tok in l:
        result.append(
            {
                "type": tok.type,
                "value": tok.value,
                "lineno": tok.lineno,
                "lexpos": tok.lexpos,
            }
        )

    return json.dumps(result)


# Parse + Interintermediate Code Generation Phase


@app.route("/yacc", methods=["POST"])
def yacc_handler():
    data = flask.request.data.decode("ASCII")

    results = {"quadruples": [], "symtables": {}}

    parser = YEPCParser()

    l = lexer.build()
    p = parser.build()

    p.parse(data, lexer=l, debug=False)

    for q in parser.quadruples:
        result = {}
        result["result"] = q.result
        result["op"] = q.op
        result["arg_one"] = q.arg_one
        result["arg_two"] = q.arg_two
        results["quadruples"].append(result)

    symtables = {}
    symtables["root"] = parser.symtables[0]

    while bool(symtables):
        name, table = symtables.popitem()
        result = {}
        for (tk, tv) in table.symbols.items():
            if isinstance(tv, str):
                result[tk] = tv
            elif isinstance(tv, SymbolTable):
                symtables[tk] = tv
                result[tk] = tv.type
        results["symtables"][name] = result

    return json.dumps(results)


@app.route("/code", methods=["POST"])
def code_handler():
    data = flask.request.data.decode("ASCII")

    parser = YEPCParser()

    l = lexer.build()
    p = parser.build()

    p.parse(data, lexer=l, debug=False)

    c_generator = YEPCToC(parser.quadruples, parser.symtables[0])

    return c_generator.to_c()


@app.route("/generate", methods=["POST"])
def generate_handler():
    data = flask.request.data.decode("ASCII")

    parser = YEPCParser()

    l = lexer.build()
    p = parser.build()

    p.parse(data, lexer=l, debug=False)

    tar_name = "yepc-%d-1820.tar.gz" % int(time.time() * 100)

    tar = tarfile.open("out/%s" % tar_name, "w:gz")
    tar.add("out/main.c", "yepc-output/main.c")
    tar.add("assets/stack.h", "yepc-output/stack.h")
    tar.add("assets/stack.c", "yepc-output/stack.c")
    tar.add("assets/Makefile", "yepc-output/Makefile")
    tar.close()

    return tar_name


@app.route("/download/<string:name>", methods=["GET"])
def download_handler(name):
    return flask.send_from_directory("out", name)
