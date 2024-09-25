class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):      # user-friendly representation
        return f"Rectangle(width={self.width}, height={self.height})"

    def __repr__(self):     # developer-friendly representation (invoked when the instance is entered directly on a REPL. (>>rectangle1)
        return f"{type(self).__name__}(width={self.width}, height={self.height})"
    # note that the string can be used to reproduce the current object

rectangle1 = Rectangle(5, 10)
rectangle2 = Rectangle(3, 4)

print(rectangle1)
print("Area:", rectangle1.area())
print("Perimeter:", rectangle1.perimeter(), end="\n\n")

print(rectangle2)    # python implicitly invokes __str__() dunder fn.
print("Area:", rectangle2.area())
print("Perimeter:", rectangle2.perimeter())

print("developer friendly representation: ", repr(rectangle1))


# Other magic methods:
# __new__
# - Operator overloading in Custom Classes methods (__add__, __sub__, __radd__, __lt__, __eq__, __contains__ etc.)
# __call__
# __len__

# resource - https://realpython.com/python-magic-methods/