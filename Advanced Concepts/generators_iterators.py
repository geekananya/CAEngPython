# an iterator is any object which implements the Iterator protocol by having a next() method that returns an object with two properties-
# 1. value: The next value in the iteration sequence.
# 2. done: This is true if the last value in the sequence has already been consumed.


# generator function
def my_gen(n):
    for i in range(3):
        yield i+3
    # yield n     # -> iterator stops here at first call. Then on next() method call, it is executed further.
    # yield n+3
    # yield n+5
obj = my_gen(6)     # a generator object is generated once, but its code is not run all at once.
print(next(obj))
print(next(obj))
print(next(obj))
print(next(obj))    # StopIteration exception (all values have been yielded)

# generator expression
g = (n for n in range(5, 10, 2))
print(next(g))
print(next(g))
print(next(g))
print(next(g))

# VS list comprehension (shorthand for creating list)
li = [n for n in range(5, 10, 2)]
print(li)   # all values are stored somewhere unlike Generator

# generator application
def fib():
     a, b = 0, 1
     while True:
         yield a
         a, b = b, a + b


# iterators : possess lazy nature        __iter__(), __next__()
list_instance = [1, 2, 3, 4]
it = iter(list_instance)
print(next(it))