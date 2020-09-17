# -*- encoding: utf-8 -*-

"""Decorator Functions for pyClass Objects"""

import inspect
from functools import wraps

def initializer(func):
    """Automatically assigns the parameters.
    
    When initializing the class, automatically initializes all the arguments.
    It is advised to be used for only thos class used for defining SQL-Tables.
    `Original-Post <https://stackoverflow.com/a/1389216>`_
    
    >>> class process:
    ...     @initializer
    ...     def __init__(self, cmd, reachable=False, user='root'):
    ...         pass
    >>> p = process('halt', True)
    >>> p.cmd, p.reachable, p.user
    ('halt', True, 'root')
    """
    names, varargs, keywords, defaults = inspect.getargspec(func)

    @wraps(func)
    def wrapper(self, *args, **kargs):
        for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
            setattr(self, name, arg)

        for name, default in zip(reversed(names), reversed(defaults)):
            if not hasattr(self, name):
                setattr(self, name, default)

        func(self, *args, **kargs)

    return wrapper