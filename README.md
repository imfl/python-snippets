# Python Snippets 代码小段

## Contents 目录

- [Lazy Function Call](#user-content-lazy-function-call)
- [Generate Lagged Values](#user-content-generate-lagged-values)
- [Catching Arguments](#user-content-catching-arguments)

## [Lazy Function Call](lazy)

A decorator that allows partial matching in function parameter names, like in R.

装饰器：像R语言一样，允许在调用函数时，对形参名称做部分匹配，不用写全形参的名称。

## [Generate Lagged Values](lag)

A helper function to generate many lagged or future values for a time series in one go. 

辅助函数：给定时间序列，一次性生成多阶滞后序列或未来序列，并且放置于同一矩阵（数据框）。

## [Catching Arguments](catch)

A decorator that catches parameter names, parameter categories, and values of the arguments passed to a function. 

装饰器：对于给定函数，捕捉调用时传入的实参，输出对应的形参名称、形参类别，以及实参的值。

## List of Source Code 源代码列表

- [Lazy Function Call](lazy/lazy.py)
- [Generate Lagged Values](lag/lag.py)
- [Catching Arguments](catch/catch.py)

_

