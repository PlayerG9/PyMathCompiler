import unittest
from src.mathcompiler import *


class Test(unittest.TestCase):
    def test_brackets(self):
        self.assertEqual(compute('7(7-2*3)'), 7)
        self.assertEqual(compute('5+7(2+1)'), 26)


if __name__ == '__main__':
    unittest.main()
