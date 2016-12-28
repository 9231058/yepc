class YEPCToC:
    def __init__(self, quadruples):
        self.quadruples = quadruples

    def to_c(self):
        c_code = ""

        c_code += "#include <stdio.h>\n"
        c_code += "int main(){\n"
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

            # line += str(op) + " " + str(arg1) + " " + str(arg2) + " "+str(result)
            c_code += line + "\n"
        c_code += "}"
        print("ouput.c generated")
        return c_code

    def make_label(self, index):
        return "L" + str(index)
