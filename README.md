# Python Snippets 代码小段

## Contents 目录

- [Lazy Function Call](#user-content-lazy-function-call)
- [Easy Generation of Lagged and Future Values for Time Series](#user-content-easy-generation-of-lagged-and-future-values-for-time-series)
- [Catching Arguments](#user-content-catching-arguments)

## Lazy Function Call

A decorator that allows partial matching in function parameter names, like in R.

Consider a function with long parameter names:

`f(x, y, population_size=1000, parsimony_coefficient=0.01)`

Typing calls like

`f(3, 5, parsimony_coefficient=0.025)`

can be tiring. If you want to be lazy, and just type

`f(3, 5, pa=0.025)`

then this decorator is for you. It allows lazy function call in this fashion.

For the source code of the decorator, click [here](lazy/lazy.py).

## Easy Generation of Lagged and Future Values for Time Series

Suppose you have a `pandas.Series` to reflect China's GDP (US$ trillion) is the past decade:

```
         gdp
2007     3.6
2008     4.6
2009     5.1
2010     6.1
2011     7.6
2012     8.6
2013     9.6
2014    10.5
2015    11.1
2016    11.2
```

You want to generate the lag-1, lag-2, and next-1 period of the figures in one go, so that you have a `pandas.DataFrame` which looks like

           gdp  gdp_lag1  gdp_lag2  gdp_next1
    2007   3.6       NaN       NaN        4.6
    2008   4.6       3.6       NaN        5.1
    2009   5.1       4.6       3.6        6.1
    2010   6.1       5.1       4.6        7.6
    2011   7.6       6.1       5.1        8.6
    2012   8.6       7.6       6.1        9.6
    2013   9.6       8.6       7.6       10.5
    2014  10.5       9.6       8.6       11.1
    2015  11.1      10.5       9.6       11.2
    2016  11.2      11.1      10.5        NaN

Then you need this helper function. For the source code, click [here](lag/lag.py).

## [Catching Arguments](catch)

**A decorator that catches parameter names, parameter categories, and values of the arguments passed to a function.** 

**装饰器：对于给定函数，捕捉调用时传入的实参，输出对应的形参名称、形参类别，以及实参的值。**

For the source code, click [here](catch/catch.py).

## List of Source Code 源代码列表

- [Lazy Function Call](lazy/lazy.py)
- [Easy Generation of Lagged and Future Values for Time Series](lag/lag.py)
- [Catching Arguments](catch/catch.py)
