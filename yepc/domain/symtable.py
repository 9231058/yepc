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
    def __init__(self):
        self.seq = 0
        self.symbols = {}

    def new_temp(self, type):
        self.seq += 1
        return 'jj' + self.seq
