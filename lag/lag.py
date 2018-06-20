'''A helper function to generate lagged or future values for a time series.'''

# Date: 18/06/20 = Wed

# Author: Fu Lei <lei dot fu at connect dot ust dot hk>

import pandas as pd


def genlag(x, *args, column=0, inplace=True, na='drop'):
    '''
    Generates lagged or future values for a time series.

    Parameters
    ----------
    x : Series or DataFrame or convertible
        Time series for lagged or future values.
        If x is DataFrame, which column to compute must be specified.

    *args : int
        1 for lag-1, 2 for lag-2,
        0 for now,  -1 for next-1 (1 period in future), and so on ...

    inplace : bool (default: True)
        - True
                keep the original time series in place, and append new columns
        - False
                generate a new DataFrame

    na : str (default: 'drop')
        - 'drop'
                drop NaN
        - 'keep'
                keep Nan
        - 'fill'
                fill NaN with zeros

    Examples
    --------
    >>> genlag([0, 1, 2, 3, 4], 0, 1, -1, inplace=False)
       now  lag1  next1
    1    1   0.0    2.0
    2    2   1.0    3.0
    3    3   2.0    4.0
    >>> genlag(china_gdp, 1, 2, -1, na='keep')
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
    '''

    if isinstance(x, pd.Series):
        df = pd.DataFrame(x) if inplace else pd.DataFrame(index=x.index)
        s = x
    elif isinstance(x, pd.DataFrame):
        if isinstance(column, int):
            s = x.iloc[:, column]
        else:
            s = x.loc[:, column]
        df = x if inplace else pd.DataFrame(index=x.index)
    else:
        try:
            x = pd.Series(x)
        except Exception:
            x = pd.DataFrame(x)
        return genlag(x, *args, column=column, inplace=inplace, na=na)

    for i in args:
        if i > 0:
            colname = 'lag' + str(i)
        elif i < 0:
            colname = 'next' + str(-i)
        else:
            colname = 'now'
        if s.name is not None:
            colname = str(s.name) + '_' + colname
        df.insert(len(df.columns), colname, s.shift(i))

    if na == 'drop':
        df.dropna(inplace=True)
    elif na == 'keep':
        pass
    elif na == 'fill':
        df.fillna(0, inplace=True)
    else:
        raise ValueError('na must be \'drop\', \'keep\', or \'fill\'')

    return df


if __name__ == '__main__':
    # for doctest
    china_gdp = pd.Series([3.6, 4.6, 5.1, 6.1, 7.6,
                           8.6, 9.6, 10.5, 11.1, 11.2],
                          index=range(2007, 2017), name='gdp')
    df = genlag(china_gdp, 1, 2, 0, -1, na='keep')
    print(df)

    import doctest
    doctest.testmod()
