# -*- coding=utf-8 -*-
import math


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


def compute(equation: str, **kwargs):
    default_compiler.compute(equation, kwargs)
