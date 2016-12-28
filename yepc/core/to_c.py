class YEPCToC:
    def __init__(self, quadruples):
        self.quadruples = quadruples

    def to_c(self):
        c_code = ""

        c_code += "#include <stdio.h>\n"
        c_code += "#include <stdlib.h>\n"
        c_code += '''
struct Node {
    int Data;
    struct Node *next;
}*top;

void popStack() {
    struct Node *temp, *var=top;
        if(var==top) {
            top = top->next;
            free(var);
        } else
            printf("\\nStack Empty");
}

void push(int value) {
    struct Node *temp;
    temp=(struct Node *)malloc(sizeof(struct Node));
    temp->Data=value;
    if (top == NULL) {
        top=temp;
        top->next=NULL;
    } else {
        temp->next=top;
        top=temp;
    }
}

void display() {
    struct Node *var=top;
    if(var!=NULL) {
        printf("\\nElements are as:\\n");
        while(var!=NULL) {
            printf("\\t%d\\n",var->Data);
            var=var->next;
        }
        printf("\\n");
    } else
        printf("\\nStack is Empty");
}\n
'''
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
            elif op == "rand":
                line += str(result) + " = rand();"
            elif op == "push":
                line += "stack_push(&%s, sizeof(%s));" % (arg1, arg2)
            elif op == "pop":
                line += "stack_pop(&%s, sizeof(%s));" % (result, arg1)
            # line += str(op) + " " + str(arg1) + " " + str(arg2) + " "+str(result)
            c_code += line + "\n"
        c_code += "}"
        print("ouput.c generated")
        return c_code

    def make_label(self, index):
        return "L" + str(index)
