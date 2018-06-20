#### Easy Generation of Lagged and Future Values for Time Series

Suppose you have a `pandas.Series` to reflect China's GDP is the past decade:

| Year | GDP (US$ Trillion) |
| ---- | ------------------ |
| 2007 | 3.5                |
| 2008 | 4.6                |
| 2009 | 5.1                |
| 2010 | 6.1                |
| 2011 | 7.6                |
| 2012 | 8.6                |
| 2013 | 9.6                |
| 2014 | 10.5               |
| 2015 | 11.1               |
| 2016 | 11.2               |

You want to generate the lag-1, lag-2, present, and next-1 period of the figures in one go, so that you have a `pandas.DataFrame` which looks like

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

Then you need this helper function. Click [here](lag.py).