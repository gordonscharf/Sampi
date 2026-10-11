import operator
import random
import importlib.util
from . import ast_nodes as a

starnderd_library = {"math", "lines"}

def add(a, b):
    ta = type(a)
    tb = type(b)

    if ta in (str, int) and tb in (str, int):
        if ta is str or tb is str:
            return f"{a}{b}"
    try:
        return a + b
    except TypeError:
        return a | b

def div(a, b):
    if b == 0:
        if a == b:
            raise ZeroDivisionError("0 cannot be divided by 0")
        return float("inf")
    ansr = a / b
    if ansr.is_integer():
        return int(ansr)
    return ansr

def in_(item, iter_):
    return item in iter_

def sgn(x):
    return (x > 0) - (x < 0)

OPS = {
    "PLUS": add,
    "MINUS": operator.sub,
    "MUL": operator.mul,
    "DIV": div,
    "POWER": operator.pow,
    "MOD": operator.mod,
    "NEG": operator.neg,

    "EQUALITY": operator.eq,
    "NOT_EQUAL": operator.ne,
    "LESS": operator.lt,
    "GREATER": operator.gt,
    "LESS_EQUAL": operator.le,
    "GREATER_EQUAL": operator.ge,

    "AND": operator.and_,
    "OR": operator.or_,
    "NOT": operator.not_,
    "IN": in_
}

names = {str: "word", int: "num", float: "num", list: "array", dict: "dict",  type(None): "none", bool: "bool"}

def get_type(x):
    return names[type(x)]

class Interpreter:
    premades = [
        ("abs", abs, 1),
        ("say", print, 1),
        ("sgn", sgn, 1),
        ("min", min, 2),
        ("max", max, 2),
        ("random", random.randint, 2),
        ("len", len, 1),
        ("get_type", get_type, 1),
        ("ask", input, 1)
        ]
    def __init__(self, path="Downloads"):
        self.vars = {"-GLOBAL-": {"true": True, "false": False, "none": None}}
        self.funcs = {}
        self.premade = {name: func for name, func, _ in self.premades}
        self.params = {name: args for name, _, args in self.premades}
        self.scope = "-GLOBAL-"
        self.path = path
        self.modules = {}
        self.keywords = {
            a.Set: self.set_,
            a.If: self.if_,
            a.Repeat: self.repeat,
            a.Until: self.until,
            a.Func: self.func,
            a.Call: self.call,
            a.Return: lambda n, _self=self: _self.fix_value(n.value),
            a.Exit: lambda n=None: a.Exit,
            a.Import: self.import_,
            a.MethodCall: self.method_call
                         }

    def interpret(self, ast):
        self.ast = ast
        for node in self.ast:
            t = type(node)
            ansr = self.keywords[t](node)
            if ansr is not None:
                return ansr

    def set_(self, node):
        name = node.name
        if type(name) is a.Index:
            parent, index = self.resolve_parent(name)
            parent[index] = self.fix_value(node.value)
        else:
            self.vars[self.scope][name] = self.fix_value(node.value)

    def if_(self, node):
        curr_ast = self.ast
        for cond, code in zip(node.conds, node.codes):
            if self.fix_value(cond):
                ansr = self.interpret(code)
                if ansr is not None:
                    return ansr
                break
        self.ast = curr_ast

    def repeat(self, node):
         curr_ast = self.ast
         use_var = node.var is not None
         var = node.var
         if type(node.num) is a.Num:
             num = range(1, int(self.fix_value(node.num)) + 1)
         else:
             num = self.fix_value(node.num)

         for i in num:
             if use_var:
                 self.vars[self.scope][var] = i
             ansr = self.interpret(node.code)
             if ansr is a.Exit:
                 break
             elif ansr is not None:
                 return ansr

         self.ast = curr_ast

    def until(self, node):
            curr_ast = self.ast
            while not self.fix_value(node.cond):
                ansr = self.interpret(node.code)
                if ansr is a.Exit:
                    break
                elif ansr is not None:
                    return ansr
            self.ast = curr_ast

    def func(self, node):
            self.funcs[node.name] = node.code
            self.params[node.name] = node.params

    def call(self, node):
            name = node.name
            if name in self.funcs:
                self.get_func_params(name, node)

                cur_scope, self.scope = self.scope, name
                curr_ast = self.ast
                self.interpret(self.funcs[name])
                self.ast = curr_ast
                self.scope = cur_scope
            elif name in self.premade:
                self.premade[name](*self.get_premade_params(name, node, self.params))

    def import_(self, node):
        name = node.name
        if name in starnderd_library:
            path = f"standard_library/{name}.py"
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.modules[node.alias] = module.new_funcs | module.new_vars
        else:
            with open(f"{self.path}/{name}.sampi") as module:
                tokens = lex(module.read())
                parser = Parser(tokens)
                ast = parser.parse()
                interpreter = Interpreter(self.path)
                interpreter.interpret(ast)
                self.modules[node.alias]


    def method_call(self, node):
        name = node.name
        obj = node.obj.name
        if obj in self.modules:
            try:
                self.modules[obj][name][0](*self.get_premade_params(name, node, {name: self.modules[obj][name][1]}))
            except KeyError:
                raise AttributeError(f"module {obj} has no function '{name}'") from None
        else:
            raise NameError(f"'{obj}' is undefined")

    def get_func_params(self, func_name, node):
        try:
            self.vars[func_name] = {"true": True, "false": False, "none": None}
            args = node.args
            for i, p in enumerate(self.params[func_name]):
                self.vars[func_name][p] = self.fix_value(args[i])
        except IndexError:
            needed_len = len(self.params[func_name])
            given_len = len(self.vars[func_name])
            raise TypeError(f"function \"{func_name}\" expected {needed_len} arguments, got {given_len}")

    def get_premade_params(self, func_name, node, params):
        try:
            args = node.args
            new_args = []
            for i in range(params[func_name]):
                new_args.append(self.fix_value(args[i]))
            return new_args
        except IndexError:
            needed_len = params[func_name]
            given_len = len(args)
            raise TypeError(f"premade \"{func_name}\" expected {needed_len} arguments, got {given_len}")

    def resolve_parent(self, index_node):
        indices = []
        node = index_node

        while type(node) is a.Index:
            indices.append(self.fix_value(node.index))
            node = node.var

        indices.reverse()
        obj = self.fix_value(node.name)

        for i in indices[:-1]:
            if type(obj)is list and i > 0:
                i -= 1
            obj = obj[i]
        last = indices[-1]
        if type(obj)is list and last > 0:
            last -= 1
        return obj, last

    def fix_value(self, value):
        t = type(value)
        if t is a.Op:
            if value.op in {"NEG", "NOT"}:
                right = self.fix_value(value.right)
                try:
                    return OPS[value.op](right)
                except TypeError:
                    raise TypeError(
                        f"{value.op} cannont bo used on {names[type(right)]}")

            left = self.fix_value(value.left)
            right = self.fix_value(value.right)
            try:
                return OPS[value.op](left, right)
            except TypeError:
                raise TypeError(
                    f"{value.op} cannot be used with {names[type(left)]} and {names[type(right)]}")

        elif t is a.Call:
            name = value.name
            if name in self.funcs:
                self.get_func_params(name, value)

                cur_scope, self.scope = self.scope, name
                curr_ast = self.ast
                result = self.interpret(self.funcs[name])
                self.ast = curr_ast
                self.scope = cur_scope
                return result
            elif name in self.premade:
                return self.premade[name](*self.get_premade_params(name, value, self.params))

            raise NameError(f"'{name}' is undefined")

        elif t is a.Var:
            name = value.name
            if name in self.vars[self.scope]:
                return self.vars[self.scope][name]
            raise NameError(f"'{name}' is undefined")

        elif t in (a.Word, a.Num):
            return value.value

        elif t is a.Array:
            return [self.fix_value(i) for i in value.value]

        elif t is a.Dict:
            return {self.fix_value(k): self.fix_value(v) for k, v in value.value.items()}

        elif t is a.Index:
            var = self.fix_value(value.var)
            og_index = self.fix_value(value.index)
            type_ = type(var) in (list, str)
            if type_ and og_index > 0:
                index = og_index - 1
            else:
                index = og_index
            try:
                if type_:
                    return var[index]
                else:
                    return var[og_index]
            except LookupError:
                raise LookupError(f"slot {og_index} is out of range")

        elif t is a.Attribute:
            name = value.name
            obj = value.obj.name
            if obj in self.modules:
                try:
                    return self.modules[obj][name]
                except KeyError:
                    raise AttributeError(f"module {obj} has no function '{name}'") from None
            else:
                raise NameError(f"'{obj}' is undefined")

        elif t is a.MethodCall:
            name = value.name
            obj = value.obj.name
            if obj in self.modules:
                try:
                    return self.modules[obj][name][0](*self.get_premade_params(name, value, {name: self.modules[obj][name][1]}))
                except KeyError:
                    raise AttributeError(f"module {obj} has no function '{name}'") from None
            elif obj in self.vars[self.scope]:
                return self.vars[self.scope]
            else:
                raise NameError(f"'{obj}' is undefined")

        raise SyntaxError(f"Unknown type '{t}'")


