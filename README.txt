How to code in Sampi ϡ

Sampi is an obsolete Greek letter and symbol for 900.
Sampi is now also high level programming language.
The symbol for sampi is ϡ.

Printing.

To bring a value, type:

say("Hello, world!")

Variables.

To set a variable, do:

set x to 1

And to increment it:

set x to x + 1

The operators are

Add 1 + 1 = 2
Subtract 1 - 1 = 0
Multiply 2 * 4 = 8
Divide 8 / 2 = 4
Exponents 4^2 = 16
And negation ~1 = -1

A string plus a number combines them

"hello" + 5 + 5 = "hello55"

Sampi does operations from left to right, and doesn't care about Pemdas

2 + 3 * 4 = 20

If you want to use Pemdas, use parentheses

2 + (3 * 4) = 14

When adding strings and numbers, be careful because

5 + 5 + "hello" = "10hello"
5 + (5 + "hello") = "55hello"

Sampi also has ways to compare values.

Equal 1 = 1 is true (do not use 1 == 1)
Greater than 1 > 1 is false
Less than 1 < 1 is false
Grater than or equal to 1 >= 1 is true
Less than or equal to 1 <= 1 is true
Not equal 1 != 1 is false

You can chain together comparisons with

And true and false is false
Ore true or false is true
Not not true is false

Sampi uses true and false, not True and False.

An if statement takes the from of

if condition:
    code
end


There is also elif and else. if comes first. you can have as many elif as as you like. else comes last, if at all.

if condition:
    code
elif condition:
    code
else condition:
    code
end

Loop look like

repeat 5:
	say("hello")
end

If you want the current iteration, do

repeat 5 as I:
    say(i)
end

It starts at 1

There is also until loops

until condition:
    code
end

It stops when the condition is true.
Be careful not to make an infinite loop.

Functions look like:

Func name arg1 arg2 arg3:
	code
end

To call a function, do

name(arg1 arg2 arg3)

Use return to get a value, or ext the function.

For example:

func add a b:
    return a + b
end

say(add(1 2))

Will say 3.

There are lists

set x to [1 2 3]
say(x[1])

Will give 1. Indexing starts a 1. 0 is the same as 1. ~1 give the last index.

Dictionary look like

set x to {1:2 3:4}
say(x[1]

Prints 2.

There is not much support for dictionaries and lists yet.
I am working on it.

I think that is all of Sampi so far.
I am moving to to a byrecode VM, 
and then will move the VM to C, for performance reasons.




