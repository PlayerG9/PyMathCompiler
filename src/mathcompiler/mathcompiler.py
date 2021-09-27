# -*- coding=utf-8 -*-
import math
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


class MathCompiler:
    def compute(self, equation: str, variables: dict) -> float:
        pass


default_compiler = MathCompiler()

compute = default_compiler.compute

# import functools
# @functools.wraps(default_compiler.compute)
# def compute(equation: str, **kwargs) -> float:
#     return default_compiler.compute(equation, kwargs)
