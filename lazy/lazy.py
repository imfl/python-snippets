'''
A decorator that allows partial matching in function parameter names, like in R

Why Use it
----------
Consider a function with long parameter names:

    f(x, y, population_size=1000, parsimony_coefficient=0.01)

Typing calls like

    f(x, y, parsimony_coefficient=0.025)

can be tiring. If you want to be lazy, and just type

    f(x, y, pa=0.025)

then this decorator is for you. It allows lazy function call in this fashion.

How to Use
----------
Put the decorator @lazy above your original function definition, like:

    @lazy
    def f(x, y, population_size=1000, parsimony_coefficient=0.01):
        ...
'''

# Author: Fu Lei <lei.fu@connect.ust.hk>

# Date: 18/06/09 = Sat

from functools import wraps
import inspect


__all__ = ['lazy']


def _partial_matching(p, names):
    '''
    Checks whether a partial name matches any of the complete names

    Parameters
    ----------
    p : str
        a partial name

    names : iterable of str
        collection of complete names

    Returns
    -------
    (m, c) : m for match result, c for complete name(s)

    | Case                    |  m | c                        |
    |-------------------------|----|--------------------------|
    | 1. Unambiguous match    |  1 | matched complete name    |
    | 2. No match             |  0 | None                     |
    | 3. Ambiguous match      | -1 | candidate complete names |

    Doctest
    -------
    # Unambiguous match

    >>> _partial_matching('pa', {'population_size', 'parsimony_coefficient'})
    (1, 'parsimony_coefficient')

    # No match

    >>> _partial_matching('pe', {'population_size', 'parsimony_coefficient'})
    (0, None)

    # Ambiguous match

    >>> names = {'population_size', 'parsimony_coefficient'}
    >>> m, c = _partial_matching('p', names)
    >>> m == -1
    True
    >>> set(c) == set({'population_size', 'parsimony_coefficient'})
    True
    '''
    c = [x for x in names if x.startswith(p)]
    m = len(c)
    if m == 1:
        c = c[0]
    elif m == 0:
        c = None
    else:
        m = -1
    return (m, c)


def lazy(f):
    '''
    A decorator that allows partial matching in function parameter names, like in R

    Essentially, it performs the conversion:

        f(*a, **partial) ==> f(*a, **complete)

    Parameter
    ---------
    f : function
        original function

    Returns
    -------
    g : function
        converts f(*a, **partial) ==> f(*a, **complete)

    Doctest
    -------
    Given a decorator @lazy and a function f so defined:

    @lazy
    def f(x, y, population_size=1000, parsimony_coefficient=0.01):
        if population_size != 1000:
            print('customized population size')
        if parsimony_coefficient != 0.01:
            print('customized parsimony coefficient')
        return x + y

    >>> f(3, 5)
    8

    >>> f(3, 5, pa=0.025)
    customized parsimony coefficient
    8

    >>> f(3, 5, po=2000)
    customized population size
    8

    >>> f(3, 5, pe=42)
    Traceback (most recent call last):
        ...
    LookupError: No match for parameter name that starts with 'pe'.
    Legal parameter name(s): ['x', 'y', 'population_size', 'parsimony_coefficient']

    >>> f(3, 5, p=2000)
    Traceback (most recent call last):
        ...
    LookupError: Ambiguous match for parameter name that starts with 'p'.
    Candidate parameter names: ['population_size', 'parsimony_coefficient']
    '''
    spec = inspect.getfullargspec(f)
    # if there is **kwargs in function signature, then lazy call is disabled
    if spec.varkw is not None:
        return f

    @wraps(f)
    def g(*a, **partial):
        complete = {}
        names = spec.args + spec.kwonlyargs
        for p in partial:
            m, c = _partial_matching(p, names)
            if m == 0:
                raise LookupError("No match for parameter name "
                                  "that starts with '%s'.\n"
                                  "Legal parameter name(s): %s"
                                  % (p, str(names)))
            elif m == -1:
                raise LookupError("Ambiguous match for parameter name "
                                  "that starts with '%s'.\n"
                                  "Candidate parameter names: %s"
                                  % (p, str(c)))
            complete[c] = partial[p]
        return f(*a, **complete)
    return g


if __name__ == '__main__':

    # for doctest
    @lazy
    def f(x, y, population_size=1000, parsimony_coefficient=0.01):
        if population_size != 1000:
            print('customized population size')
        if parsimony_coefficient != 0.01:
            print('customized parsimony coefficient')
        return x + y

    import doctest
    doctest.testmod()
