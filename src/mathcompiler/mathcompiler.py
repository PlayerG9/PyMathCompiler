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
    variables: dict

    def __init__(self, functions: dict, constants: dict):
        self.functions = functions
        self.constants = constants

    def compute(self, equation: str, variables: dict, auto_round: bool = True) -> float:
        self.variables = variables
        try:
            formula = self.compile(equation)
            result = self.solve(formula, variables)
        finally:
            del self.variables  # remove attribute

        if auto_round and result % 1 == 0:
            return int(result)
        else:
            return result

    def compile(self, equation: str) -> t.List:
        pass

    def solve(self, formula: list, variables: dict) -> float:
        pass


class Number:
    def __init__(self, val: str):
        try:
            self.val = float(val)  # parse float (ex 14.9)
        except ValueError:
            try:
                self.val = float(int(val))  # parse int (to float) (ex 8)
            except ValueError:
                raise NumberParseError("can't parse {!r}".format(val))


class Variable:
    def __init__(self, val: str, consts: dict):
        try:
            self.val = consts[val]
        except KeyError:
            raise VariableMissingError("can't find {!r}".format(val))


class Snipped:
    def __init__(self, equation: str, compiler: MathCompiler):
        self.equation = equation
        self.compiler = compiler

    @property
    def val(self):
        result = self.compiler.compute(self.equation, self.compiler.variables, auto_round=False)
        return result


class Function(Snipped):
    def __init__(self, name: str, equation: str, compiler: MathCompiler):
        super().__init__(equation, compiler)
        try:
            self.callback = compiler.functions[name]
        except KeyError:
            raise FunctionMissingError("can't find {!r}".format(name))

    @property
    def val(self):
        result = super().val
        return self.callback(result)


class Brackets(Snipped):
    pass


default_compiler = MathCompiler(default_functions, default_constants)


@functools.wraps(default_compiler.compute)
def compute(equation: str, **kwargs) -> float:
    return default_compiler.compute(equation, kwargs)
