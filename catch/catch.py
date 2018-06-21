# -*- coding: utf-8 -*-
"""
A decorator that catches parameter names, parameter categories, and values of
the arguments passed to a function.
"""

# Date: 18/06/21 = Thu

# Author: Fu Lei <lei dot fu at connect dot ust dot hk>

import functools
import copy
import inspect

__all__ = ['catch']


def catch(debug=True):
    """
    A decorator that catches parameter names, parameter categories, and values
    of the arguments passed to a function.

    How to Use
    ----------
    Put the decorator @catch(), or @catch(debug=True), above function
    definition. To turn off catching, set @catch(debug=False), so that the
    decorator does nothing.

    What Does it Do
    ---------------
    Prints out the names, categories and values of the arguments. The arguments
    fall into 4 categories:
        1. arguments for positional-or-keyword parameters
        2. arguments for keyword-only parameters
        3. arguments for var-positional parameters
        4. arguments for var-keyword parameters

    References
    ----------
    https://docs.python.org/3/glossary.html#term-parameter
    """
    def do(f):
        @functools.wraps(f)
        def g(*args, **kwargs):
            local = copy.deepcopy(locals())
            spec = inspect.getfullargspec(f)
            print(line('Start Catching Arguments Passed to Function %s()'
                       % f.__name__, p=':'))

            # build dict for arguments for positional-or-keyword parameters
            poskey = {}
            i = j = 0
            for x in spec.args:
                try:
                    poskey[x] = local['args'][i]
                    i += 1
                except IndexError:
                    try:
                        poskey[x] = local['kwargs'][x]
                        del local['kwargs'][x]
                    except KeyError:
                        poskey[x] = spec.defaults[j]
                        j += 1
            if len(poskey) > 0:
                print(line('Arguments for Positional-or-Keyword Parameters'))
                for x in poskey:
                    print(x, '=', poskey[x])

            # build dict for arguments for keyword-only parameters
            keyonly = {}
            for x in spec.kwonlyargs:
                try:
                    keyonly[x] = local['kwargs'][x]
                    del local['kwargs'][x]
                except KeyError:
                    keyonly[x] = spec.kwonlydefaults[x]
            if len(keyonly) > 0:
                print(line('Arguments for Keyword-Only Parameters'))
                for x in keyonly:
                    print(x, '=', keyonly[x])

            # build tuple for arguments for var-positional parameters
            varpos = local['args'][i:]
            if len(varpos) > 0:
                print(line('Arguments for Var-Positional Parameters'))
                print(varpos)

            # build dict for arguments for var-keyword parameters
            varkey = local['kwargs']
            if len(varkey) > 0:
                print(line('Arguments for Var-Keyword Parameters'))
                for x in varkey:
                    print(x, '=', varkey[x])

            print(line('Finish Catching Arguments Passed to Function %s()'
                       % f.__name__, p=':'))
            return f(*args, **kwargs)
        return g

    def dont(f):
        def g(*args, **kwargs):
            return f(*args, **kwargs)
        return g

    return do if debug else dont


@catch()  # equivalent to @catch(debug=True)
def foo(a, b=98, *, c, d=100, e, **f):
    """
    Function to test decorator @catch().

    | parameter name     | type                  | with default value |
    | ------------------ | --------------------- | ------------------ |
    | a                  | positional-or-keyword | no                 |
    | b                  | positional-or-keyword | yes                |
    | c                  | keyword-only          | no                 |
    | d                  | keyword-only          | yes                |
    | e                  | keyword-only          | no                 |
    | f, g, ... (if any) | var-keyword           | no                 |
    """
    print('a = ', a)
    print('b = ', b)
    print('c = ', c)
    print('d = ', d)
    print('e = ', e)
    print('f = ', f)  # f is a dict for var-keyword parameters
    print(line('', p='.'))


@catch()  # equivalent to @catch(debug=True)
def bar(a=97, *b):
    """
    Function to test decorator @catch().

    | parameter name     | type                  | with default value |
    | ------------------ | --------------------- | ------------------ |
    | a                  | positional-or-keyword | yes                |
    | b                  | var-positoinal        | no                 |
    """
    print('a = ', a)
    print('b = ', b)
    print(line('', p='.'))


def line(s='', p='-', length=75, lead=5, newline=True):
    if len(s) > 0:
        s = ' ' + s + ' '
    t = '%s%s%s' % (p * lead, s, p * (length - lead - len(s)))
    return '\n' + t + '\n' if newline else t


# tests
if __name__ == '__main__':
    foo(0, 1, c=2, d=3, e=4, f=5, g=6)
    foo(0, c=2, e=4)
    bar(3, 6, 66, 666, 6666, 66666, 666666)
    bar()
