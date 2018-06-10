# Python Snippets 代码片段

## [Lazy Call](lazy/lazy.py)

A decorator that allows partial matching in function parameter names, like in R

Consider a function with long parameter names:
    `f(x, y, population_size=1000, parsimony_coefficient=0.01)`
Typing calls like
    `f(x, y, parsimony_coefficient=0.025)`
can be tiring. If you want to be lazy, and just type
    `f(x, y, pa=0.025)`
then this decorator is for you. It allows lazy function call in this fashion.


