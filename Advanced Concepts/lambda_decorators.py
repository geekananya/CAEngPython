absolute_val = lambda n : n if n>0 else -n      # single line anonymous function
print(absolute_val(9))
print(absolute_val(-12))


#decorators

# Functions are treated as FIRST CLASS OBJECTS,
# and can be passed as arguments to another fn, defined inside another fn and returned by another fn.
def outer(n):
    def inner():
        return "hi im the inner fn"
    if n==1:
        return inner
    else:
        return "Outer fn"

# print(outer(1)())
# print(outer(0))

from random import random

def print_name():
    print('ABCDE')

def decorator(fn):
    def wrapper():
        print('*'*10)
        fn()
        print('_'*10)
    return wrapper()

decorator(print_name)

# -- study: decorator with arguments (decorated fn has args)

@decorator              #decorates and calls fn
def print_random():
    print(random())