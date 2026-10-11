import math

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def asin(x):
    return math.degrees(math.asin(x))

def acos(x):
    return math.degrees(math.acos(x))

def atan(x):
    return math.degrees(math.atan(x))

def atan2(y, x):
    return math.degrees(math.atan2(y, x))

new_vars = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "atan2": atan2,
    "hypot": math.hypot,
    "pi": 3.141592653589793,
    "tau": 6.283185307179586,
    "e": 2.718281828459045,
    }
