from ..domain.symtable import SymbolTable


class YEPCToC:
    def __init__(self, quadruples, symtable):
        self.quadruples = quadruples
        self.symtable = symtable

    def to_c(self):
        c_code = ""

        # Includes :)
        c_code += "#include <stdio.h>\n"
        c_code += "#include <stdlib.h>\n"
        c_code += '\n'
        c_code += '#include "stack.h"\n'
        c_code += '\n'

        # Variable declaration based on BFS
        q = []
        q.append(self.symtable)
        while bool(q):
            t = q.pop()
            for symbol in t.symbols:
                if isinstance(t.symbols[symbol], str):
                    c_code += '%s %s;\n' % (t.symbols[symbol], t.get_symbol_name(symbol))
                elif isinstance(t.symbols[symbol], SymbolTable):
                    s = t.symbols[symbol]
                    if s.type == 'record':
                        c_code += 'struct %s {\n' % s.name[1:]
                        for (name, type) in s.symbols.items():
                            if type[0] == '#':
                                type = type[1:]
                            c_code += "\t%s %s;\n" % (type, name[1:])
                        c_code += '};\n'
                    else:
                        q.append(s)
        c_code += '\n'

        # QuadRuples to code
        c_code += "int main(){\n"
        c_code += "\tstruct stack *yepc_stack;\n"
        c_code += "\n"
        c_code += "\tyepc_stack = stack_create();\n"
        for i in range(len(self.quadruples)):
            entry = self.quadruples[i]
            label = self.make_label(i) + ":"
            op = entry.op
            arg1 = entry.arg_one
            arg2 = entry.arg_two
            result = entry.result
            line = label + " "

            if op == 'if':
                line += "if (" + str(arg1) + ")"
            elif op == 'goto':
                line += "goto " + self.make_label(arg1) + ";"
            elif op == '+':
                line += str(result) + " = " + str(arg1) + " + " + str(arg2) + ";"
            elif op == '-':
                line += str(result) + " = " + str(arg1) + " - " + str(arg2) + ";"
            elif op == '*':
                line += str(result) + " = " + str(arg1) + " * " + str(arg2) + ";"
            elif op == '/':
                line += str(result) + " = " + str(arg1) + " / " + str(arg2) + ";"
            elif op == '%':
                line += str(result) + " = " + str(arg1) + " % " + str(arg2) + ";"
            elif op == "=":
                line += str(result) + " = " + str(arg1) + ";"
            elif op == "rand":
                line += str(result) + " = rand();"
            elif op == "push":
                line += "stack_push(yepc_stack, &%s, sizeof(%s));" % (arg1, arg2)
            elif op == "pop":
                line += "stack_pop(yepc_stack, &%s, sizeof(%s));" % (result, arg1)
            # line += str(op) + " " + str(arg1) + " " + str(arg2) + " "+str(result)
            c_code += "\t" + line + "\n"
        c_code += "}"
        print("ouput.c generated")
        return c_code

    def make_label(self, index):
        return "L" + str(index)
