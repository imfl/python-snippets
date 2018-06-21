# Catching Arguments

**A decorator that catches parameter names, parameter categories, and values of the arguments passed to a function.** 

**装饰器：对于给定函数，捕捉调用时传入的实参，输出对应的形参名称、形参类别，以及实参的值。**

Suppose you have a function with signature `foo(a, b=500, *c, d=50, e, f=5, **g)`.

Let's say you call it with `foo(0, 1, 2, 22, 222, 2222, d=3, e=4, g=6, h=7, i=8, j=9, k=10)`.

If you want a clear print-out to show you what values are passed to which parameters, like:

```
----- Arguments for Positional-or-Keyword Parameters ----------------------

a = 0
b = 1  (default = 500)

----- Arguments for Var-Positional Parameters -----------------------------

c --> (2, 22, 222, 2222)

----- Arguments for Keyword-Only Parameters -------------------------------

d = 3  (default = 50)
e = 4
f = 5  (default = 5)

----- Arguments for Var-Keyword Parameters --------------------------------

g -->
{
    g = 6
    h = 7
    i = 8
    j = 9
    k = 10
}
```

then you may need this decorator.

Get [source code](catch.py).
