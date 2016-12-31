# In The Name Of God
# ========================================
# [] File Name : symtable.py
#
# [] Creation Date : 08-12-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
#
# [] Created By : Saman Fekri (Samanf74@gmail.com)
# =======================================


class SymbolTable:
    scope_seq = 0

    '''
    Provides symbol table in our front end compiler

    | Symbol | Type |
    |:------:|:----:|
    | jj1    | int  |

    '''
    def __init__(self, parent, type, name=None):
        self.symbols = {}
        self.header = {}
        self.meta = {}
        self.parent = parent
        self.temp_id_generator = self.temp_id_generator()
        self.type = type
        if name is None:
            self.name = 'scp' + str(SymbolTable.scope_seq)
            SymbolTable.scope_seq += 1
        else:
            self.name = name

    def temp_id_generator(self):
        seq = 0
        while True:
            yield '#jj' + str(seq)
            seq += 1

    def new_temp(self, temp_type):
        temp_id = next(self.temp_id_generator)
        self.symbols[temp_id] = temp_type
        return temp_id

    def insert_variable(self, var_id, var_type: str):
        self.symbols[var_id] = var_type

    def insert_scope(self, scope_table):
        self.symbols[scope_table.name] = scope_table

    def insert_procedure(self, proc_table):
        proc_id = proc_table.name
        self.symbols[proc_id] = proc_table

    def get_parent_function(self):
        current = self
        while current.type != 'function':
            current = current.parent
        return current

    def get_symbol_type(self, symbol):
        current = self
        result = current.symbols.get(symbol, None)
        while result is None:
            if current.parent is not None:
                current = current.parent
            else:
                raise KeyError(symbol)
            result = current.symbols.get(symbol, None)
        return result

    def get_symbol_name(self, symbol):
        '''
        Get fully qualified name for your given symbol
        if it exists in symbol table hierarchy.
        '''
        if not isinstance(symbol, str) or symbol[0] != '#':
            return symbol
        current = self
        result = current.symbols.get(symbol, None)
        while result is None:
            if current.parent is not None:
                current = current.parent
            else:
                raise KeyError(symbol)
            result = current.symbols.get(symbol, None)
        return current.generate_symbol_name(symbol)

    def get_symbol_meta(self, symbol):
        current = self
        result = current.meta.get(symbol, None)
        while result is None:
            if current.parent is not None:
                current = current.parent
            else:
                raise KeyError(symbol)
            result = current.meta.get(symbol, None)
        return result

    def generate_symbol_name(self, name):
        '''
        Generate fully qualified name for your given name
        based on symbol table hierarchy.
        '''
        if name[0] == '#':
            name = name[1:]
        current = self
        while current is not None:
            if current.name[0] == '#':
                scope_name = current.name[1:]
            else:
                scope_name = current.name
            name = scope_name + '_' + name
            current = current.parent
        return name
