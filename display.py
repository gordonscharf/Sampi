import sampi

code = """
repeat 5 as i:
    say("hello")
end
"""

tokens = sampi.lex(code)
parser = sampi.Parser(tokens)
ast = parser.parse()
compiler = sampi.Compiler()
byte_code = compiler.compile_(ast)
vars_ = sampi.run_vm(byte_code)
