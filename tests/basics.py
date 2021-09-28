import unittest
from src.mathcompiler import *


class Test(unittest.TestCase):
    def test_number(self):
        r"""
        test 10 random numbers
        """
        import random

        for i in range(10):
            num = random.randint(0, 100)
            got = compute(str(num))
            self.assertEqual(num, got)

    def test_constant(self):
        r"""

        """
        import math

        self.assertEqual(compute('pi'), math.pi)
        self.assertEqual(compute('e'), math.e)
        self.assertEqual(compute('inf'), math.inf)
        self.assertEqual(compute('-inf'), -math.inf)

    def test_addition(self):
        import random

        for i in range(10):
            a = random.randint(0, 100)
            b = random.randint(0, 100)
            got = compute('{}+{}'.format(a, b))
            self.assertEqual(got, a+b)

    def test_subtraction(self):
        import random

        for i in range(10):
            a = random.randint(0, 100)
            b = random.randint(0, 100)
            got = compute('{}-{}'.format(a, b))
            self.assertEqual(got, a+b)

    def test_multiplication(self):
        import random

        for i in range(10):
            a = random.randint(0, 100)
            b = random.randint(0, 100)
            got = compute('{}*{}'.format(a, b))
            self.assertEqual(got, a+b)

    def test_division(self):
        import random

        for i in range(10):
            a = random.randint(0, 100)
            b = random.randint(0, 100)
            got = compute('{}/{}'.format(a, b))
            self.assertEqual(got, a+b)

    def test_brackets(self):
        self.assertEqual(compute('3*(4-2)'), 6)

    def test_variables(self):
        self.assertEqual(compute('x', x=5), 5)
        self.assertEqual(compute('2*x', x=5), 10)
        self.assertEqual(compute('3x', x=5), 15)


if __name__ == '__main__':
    unittest.main()
