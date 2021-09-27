# -*- coding=utf-8 -*-
import math
import re
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

default_dict = {**default_functions, **default_constants}  # combine both


class MathCompiler:
    def compute(self, equation: str, variables: dict) -> float:
        pass


default_compiler = MathCompiler()

compute = default_compiler.compute

# import functools
# @functools.wraps(default_compiler.compute)
# def compute(equation: str, **kwargs) -> float:
#     return default_compiler.compute(equation, kwargs)
