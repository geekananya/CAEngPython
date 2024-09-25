import unittest
from calc import *

class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(-4, 17), 13)
        self.assertEqual(add(-1, -1), -2)
        self.assertEqual(add(-3, 3), 0)
        self.assertEqual(add(5, 0), 5)

    def test_subtract(self):
        self.assertEqual(subtract(-4, 17), -21)
        self.assertEqual(subtract(-1, -1), 0)
        self.assertEqual(subtract(-3, 3), -6)
        self.assertEqual(subtract(-3, 0), -3)

    def test_multiply(self):
        self.assertEqual(multiply(-4, 17), -68)
        self.assertEqual(multiply(-1, -1), 1)
        self.assertEqual(multiply(-3, 3), -9)
        self.assertEqual(multiply(0, 3), 0)

    def test_divide(self):
        self.assertEqual(divide(-4, 16), -0.25)
        self.assertEqual(divide(-1, -1), 1)
        self.assertEqual(divide(0, 4), 0)
        self.assertEqual(divide(5, 2), 2.5)

        with self.assertRaises(ValueError):
            divide(12, 0)

if __name__ == "__main__":
    unittest.main()