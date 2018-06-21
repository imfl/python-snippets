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
    Put the @catch(), or @catch(debug=True), above the defitnition of the
    function to decorate. To turn off catching, set @catch(debug=False), so
    that the decorator does nothing.

    What Does it Do
    ---------------
    Prints out the parameter names, parameter categories, and values of the
    arguments passed to a function. The arguments fall into 4 categories:
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
                j = 0 if spec.defaults is None else len(spec.defaults)
                j -= len(spec.args)
                for x in poskey:
                    print(x, '=', poskey[x], end='')
                    if j >= 0:
                        print('  (default = ', spec.defaults[j], ')', sep='')
                    else:
                        print('')
                    j += 1

            # build tuple for arguments for var-positional parameters
            varpos = local['args'][i:]
            if len(varpos) > 0:
                print(line('Arguments for Var-Positional Parameters'))
                print(spec.varargs, '-->', varpos)

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
                    print(x, '=', keyonly[x], end='')
                    if x in spec.kwonlydefaults:
                        print('  (default = ', spec.kwonlydefaults[x], ')',
                              sep='')
                    else:
                        print('')

            # build dict for arguments for var-keyword parameters
            varkey = local['kwargs']
            if len(varkey) > 0:
                print(line('Arguments for Var-Keyword Parameters'))
                print(spec.varkw, '-->\n{')
                for x in varkey:
                    print('   ', x, '=', varkey[x])
                print('}')

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
def foo(a, b=500, *c, d=50, e, f=5, **g):
    """
    Function to test decorator @catch().

    | parameter name     | type                  | with default value |
    | ------------------ | --------------------- | ------------------ |
    | a                  | positional-or-keyword | no                 |
    | b                  | positional-or-keyword | yes                |
    | c --> ... (if any) | var-positional        | no                 |
    | d                  | keyword-only          | yes                |
    | e                  | keyword-only          | no                 |
    | f                  | keyword-only          | yes                |
    | g --> ... (if any) | var-keyword           | no                 |
    """
    print('a =', a)
    print('b =', b)
    print('c =', c)         # c is a tuple
    print('d =', d)
    print('e =', e)
    print('f =', f)
    print('g =', g)         # g is a dict


def line(s='', p='-', length=75, lead=5, newline=True):
    if len(s) > 0:
        s = ' ' + s + ' '
    t = '%s%s%s' % (p * lead, s, p * (length - lead - len(s)))
    return '\n' + t + '\n' if newline else t


# tests
if __name__ == '__main__':
    foo(0, 1, 2, 22, 222, 2222, d=3, e=4, g=6, h=7, i=8, j=9, k=10)
    foo(a='a', e=2.71828)
