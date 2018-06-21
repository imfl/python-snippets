# Catching Arguments

**A decorator that catches parameter names, parameter categories, and values of the arguments passed to a function.** 

**装饰器：对于给定函数，捕捉调用时传入的实参，输出对应的形参名称、形参类别，以及实参的值。**

Suppose you have a function with signature `foo(a, b=98, *, c, d=100, e, **f)`.

Let's say you call it with `foo(0, 1, c=2, d=3, e=4, f=5, g=6)`.

You want to know what values are passed to which parameters, like:

```
----- Arguments for Positional-or-Keyword Parameters ----------------------

a = 0
b = 1  (default = 98)

----- Arguments for Keyword-Only Parameters -------------------------------

c = 2
d = 3  (default = 100)
e = 4

----- Arguments for Var-Keyword Parameters --------------------------------

f -->
{
    f = 5
    g = 6
}
```

Consider another case, a function with signature `bar(a=97, *b)`. 

Now you call it with `bar(3, 6, 66, 666, 6666, 66666, 666666)`.

If you want a clean-cut print-out like:

```
----- Arguments for Positional-or-Keyword Parameters ----------------------

a = 3  (default = 97)

----- Arguments for Var-Positional Parameters -----------------------------

b --> (6, 66, 666, 6666, 66666, 666666)
```

then you may need this decorator.

Get [source code](catch.py).

