# -*- coding=utf-8 -*-
r"""
# noinspection PyTypeChecker
"""
import math
import re
import functools
import typing as t
import logging
from .exceptions import *


logging.getLogger(__package__).setLevel(logging.WARNING)


default_functions = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'pow': math.pow,
    'sqrt': math.sqrt,
}

default_constants = {
    'pi': math.pi,
    'e': math.e,
    'inf': math.inf
}

# default_dict = {**default_functions, **default_constants}  # combine both


class MathCompiler:
    solve_braces = re.compile(r'')
    solve_dots = re.compile(r'')
    solve_lines = re.compile(r'')
    solve_statement = re.compile(r'')

    def __init__(self, functions: dict, constants: dict):
        self.functions = functions
        self.constants = constants

    def compute(self, equation: str, variables: dict, auto_round: bool = True) -> float:
        formula = self.compile(equation)
        result = self.solve(formula, variables)

        if auto_round and result % 1 == 0:
            return int(result)
        else:
            return result

    def compile(self, equation: str) -> t.List:
        pass

    def solve(self, formula: list, variables: dict) -> float:
        pass


default_compiler = MathCompiler(default_functions, default_constants)


@functools.wraps(default_compiler.compute)
def compute(equation: str, **kwargs) -> float:
    return default_compiler.compute(equation, kwargs)
