from . import ast_nodes as a

class Compiler():
    def __init__(self):
        self.byte_code = []
        self.loop = 0
        self.minus = 0
        self.lookups = {
            a.Set: self.set_,
            a.Glue: self.glue,
            a.If: self.if_,
            a.Repeat: self.repeat,
            a.Func: self.func,
            a.Return: self.return_,
            a.Until: self.until,
            a.Import: lambda node: ("IMPORT", node.name, node.alias),

            a.Op: self.op,
            a.Call: self.call,
            a.MethodCall: self.methodcall,

            a.Number: lambda node: ("CONST", node),
            a.String: lambda node: ("CONST", node),
            a.Array: self.array,
            a.Dict: self.Dict,
            a.Index: self.index,
            a.Var: lambda node: ("GET", node.name),
            a.Attribute: self.attribute,

            str: lambda node: None
            }

    @property
    def length(self): # allways use self.legth to get the current index
        return len(self.byte_code) - self.minus

    def emit(self, instruction):
        index = len(self.byte_code) # do not use self.index here. we want the acctual index
        self.byte_code.append(instruction)
        return index

    def patch(self, index, target):
        self.byte_code[index] = (
            self.byte_code[index][0],
            target
        )

    def compile_(self, ast):
        for node in ast:
            ansr = self.lookups[type(node)](node)
            if ansr is not None:
                self.byte_code.append(ansr)
        return self.byte_code

    def mini_compile(self, node):
        ansr = self.lookups[type(node)](node)
        if ansr is not None:
            self.byte_code.append(ansr)

    def set_(self, node):
        self.mini_compile(node.value)
        return "STORE", node.name
    
    def glue(self, node):
        self.mini_compile(node.value)
        return "GLUE", node.name

    def op(self, node):
        self.mini_compile(node.left)
        self.mini_compile(node.right)
        return node.op,

    def call(self, node):
        self.compile_(node.args)
        return "CALL", node.name, len(node.args)

    def if_(self, node):
        jump_indexs = []

        for condition, code in zip(node.conds, node.codes):
            self.mini_compile(condition)
            jump_index = self.emit(("JUMP_IF_FALSE", None))
            self.compile_(code)

            jump_indexs.append(self.emit(("JUMP", None)))
            self.patch(jump_index, self.length)

        target = self.length
        for jump_index in jump_indexs:
            self.patch(jump_index, target)

    def repeat(self, node):
        var = f"!{self.loop}"
        self.byte_code.append(("INIT_LOOP", var))
        start = self.length
        self.mini_compile(node.num)
        index = self.emit(("LOOP_NEXT", None, var))

        self.loop += 1
        self.compile_(node.code)
        self.byte_code.append(("JUMP", start))
        self.patch(index, target)
        self.loop -= 1

    def func(self, node):
        self.byte_code.append(("START_FUNC", node.name))
        index = self.length # this allows sub functions
        self.minus += index
        self.compile_(node.code)
        self.byte_code.append(("END_FUNC", node.params))
        self.minus -= index

    def return_(self, node):
        self.mini_compile(node.value)
        return "RETURN",

    def index(self, node):
        self.mini_compile(node.var)
        self.mini_compile(node.index)
        return "INDEX",

    def until(self, node):
        start_index = self.length
        self.mini_compile(node.cond)
        jump_index = self.emit(("JUMP_IF_TRUE", None))
        self.compile_(node.code)
        self.byte_code.append(("JUMP", start_index))
        self.patch(jump_index, self.length)
    
    def attribute(self, node):
        self.mini_compile(node.obj)
        return "ATTRIBUTE", node.name
    
    def methodcall(self, node):
        self.mini_compile(node.obj)
        self.compile_(node.args)
        return "METHOD_CALL", node.name, len(node.args)
    
    def array(self, node):
        self.compile_(node._list())
        return "ARRAY", len(node)
    
    def Dict(self, node):
        self.compile_([x for pair in node.items() for x in pair])
        return "DICT", len(node)
