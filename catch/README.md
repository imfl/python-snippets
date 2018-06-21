# Catching Names, Values, and Categories of Arguments

Suppose you have a function with signature `foo(a, b=98, *, c, d=100, e, **f)`.

In calling it, you want to know what values are passed to which parameters. The situation may become complex when *var-positional* parameters (`*`)  and *var-keyword* parameters (`**`) are involved. 

Let's say you call with `foo(0, 1, c=2, d=3, e=4, f=5, g=6)`.

You want a clean-cut print-out like:

```
----- Arguments for Positional-or-Keyword Parameters ----------------------

a = 0
b = 1

----- Arguments for Keyword-Only Parameters -------------------------------

c = 2
d = 3
e = 4

----- Arguments for Var-Keyword Parameters --------------------------------

f = 5
g = 6
```

As another case, consider another function with signature `bar(a=97, *b)`.

Let's say you call with `bar(3, 6, 66, 666, 6666, 66666, 666666)`.

You want a clean-cut print-out like:

```
----- Arguments for Positional-or-Keyword Parameters ----------------------

a = 3

----- Arguments for Var-Positional Parameters -----------------------------

(6, 66, 666, 6666, 66666, 666666)
```

Then you need this decorator. For the source code, click [here](catch.py).

