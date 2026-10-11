# **How to code in Sampi**

Sampi is an obsolete Greek letter and symbol for 900.
Sampi is now also high level programming language.
The symbol for sampi is ϡ.

## **Installing Sampi**

Download the Sampi using the green Code button on 
GitHub and select Download ZIP. Extract the downloaded folder.

## **Running Sampi**
To run Sampi, you will need Python3.
Open a terminal in the project folder and run:

python3 IDE.py

Or use run IDE.py in python.
Once the IDE opens, you can begin experimenting with Sampi.

## **Printing**

To bring a value, type:
```text
say("Hello, world!")
```

## **Variables**

To set a variable, do:
```text
set x to 1
```
And to increment it:
```text
set x to x + 1
```
## **Operators**

| Operation | Example | Result |
|---|---|---|
| Addition | `1 + 1` | `2` |
| Subtraction | `3 - 1` | `2` |
| Multiplication | `2 * 4` | `8` |
| Division | `8 / 2` | `4` |

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

And: true and false is false
Or: true or false is true
Not: not true is false

Sampi uses true and false, not True and False.

## **If Statments**

An if statement takes the from of
```text
set x to 1
if x = 1:
    say("x is equal to 1!")
end
```

There is also else. if comes first. else comes last, if at all.
```text
set num to 1

if num > 0:
    say("+")
else if x = 0:
    say("0")
else:
    say("-")
end
```

## **Loops**
 ```text
repeat 5:
	say("hello")
end
```

If you want the current iteration, do
```text
repeat 5 as I:
    say(i)
end
```

It starts at 1

There is also until loops
```text
set guess to ""
until guess = "Password:
    say("That ie not the password")
	set guess to ask("What is the password? ")
end
```

It stops when the condition is true.
Be careful not to make an infinite loop.

## **Functions**
```text
func greet name:
	say("Hello, " + name + "!")
end
```

To call a function, do
```text
greet(1, 2)
```

Use return to get a value, or exit the function.

For example:
```text
func add a b:
    return a + b
end

say(add(1, 2))
```

Will say 3.

## **Multisets**

lists are made with square brackets.
```text
set x to [1, 2, 3]
say(x[1])
```

Will give 1. Indexing starts a 1. 0 is the same as 1. ~1 give the last index.

Dictionary's are made with curly braces.

```text
set x to {"a":1, "b":2}
say(x["a"])
```

Prints 1.

There is not much support for dictionaries and lists yet.
I am working on it.

I am moving to to a bytecode VM, 
and then will move the VM to C, for performance reasons.




