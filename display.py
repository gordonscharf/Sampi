import sampi

code = """
say(~1^0.5)
"""

tokens = sampi.lex(code)
parser = sampi.Parser(tokens)
ast = parser.parse()
compiler = sampi.Compiler()
byte_code = compiler.compile_(ast)
x = sampi.run_vm(byte_code)