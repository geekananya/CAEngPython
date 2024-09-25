class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def describe(self):
        return f"Rectangle(width={self.width}, height={self.height})"

rectangle1 = Rectangle(5, 10)
rectangle2 = Rectangle(3, 4)

print(rectangle1.describe())
print("Area:", rectangle1.area())
print("Perimeter:", rectangle1.perimeter(), end="\n\n")

print(rectangle2.describe())
print("Area:", rectangle2.area())
print("Perimeter:", rectangle2.perimeter())