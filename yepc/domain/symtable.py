# In The Name Of God
# ========================================
# [] File Name : symtable.py
#
# [] Creation Date : 08-12-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================


class SymbolTable():
    '''
    Provides symbol table in our front end compiler

    | Symbol | Type |
    |:------:|:----:|
    | jj1    | int  |

    '''
    def __init__(self, parent):
        self.seq = 0
        self.symbols = {}
        self.header = {}
        self.parent = parent

    def new_temp(self, temp_type):
        self.seq += 1
        temp_id = 'jj' + self.seq
        self.symbols[temp_id] = temp_type
        return temp_id

    def insert_variable(self, var_id, var_type):
        self.symbols[var_id] = var_type

    def insert_procedure(self, proc_id, proc_table):
        self.symbols[proc_id] = proc_table

    def add_width(self, width):
        self.header[width] = width
