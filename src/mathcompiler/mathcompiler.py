# -*- coding=utf-8 -*-
r"""
# noinspection PyTypeChecker
"""
import math
import re
import operator
import functools
import typing
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


operator_index = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
}


class MathCompiler:
    _token_index = [
        ("NUMBER", r'\d+(\.\d+)?'),
        ("OPERATOR", r'[%s]' % re.escape(''.join(operator_index.keys()))),
        ("FUNCTION", r'[\w^\d]\w*\(.+\)'),
        ("CONSTANT", r'[\w^\d]\w*'),
        ("BRACKETS", r'\((.+)\)'),
    ]
    _token_regex = re.compile(r'|'.join('(?P<%s>%s)' % pair for pair in _token_index), re.ASCII)
    _funcsplit = re.compile(r'^(?P<name>[\w^\d]\w*)\((?P<equation>.+)\)$', re.ASCII)
    _bracketfinder = re.compile(r'(?P<ignore>[\w^\d]\w*\()|(?P<bracket>\()', re.ASCII)
    variables: dict

    def __init__(self, functions: dict, constants: dict):
        self.functions = functions
        self.constants = constants

    def compute(self, equation: str, variables: dict, auto_round: bool = True) -> float:
        self.variables = variables
        # try:
        formula = self.compile(equation)
        result = self.solve(formula)
        # finally:
        #     del self.variables  # remove attribute

        if auto_round and result % 1.0 == 0.0:
            return int(result)
        else:
            return result

    def compile(self, equation: str) -> typing.List:
        pre = []

        i = 0
        level = 0

        m = self._bracketfinder.search(equation, i)

        while m:
            # print(m.groupdict())
            # print(m.lastgroup)
            a, i = m.span()
            if m.lastgroup != 'ignore':
                pre.append(equation[:a])
                level += 1
                try:
                    while level > 0:
                        i += 1
                        if equation[i] == '(':
                            level += 1
                        elif equation[i] == ')':
                            level -= 1
                except IndexError:
                    raise MissingBracketError()
                pre.append(self.compute(equation[a + 1:i], self.variables))
                i += 1
            m = self._bracketfinder.search(equation, i)
        else:
            stuff = equation[i:]
            if stuff:
                pre.append(stuff)

        equation = ''.join(str(e) for e in pre)

        back = []

        for token in self._token_regex.finditer(equation):
            kind = token.lastgroup
            value = token.group()
            # print([kind, value])
            if kind == 'NUMBER':
                back.append(Number(value))
            elif kind == 'OPERATOR':
                back.append(Operator(value))
            elif kind == 'FUNCTION':
                m = self._funcsplit.fullmatch(value)
                n, e = m.groups()
                back.append(Function(n, e, self))
            elif kind == 'CONSTANT':
                back.append(Variable(value, self))
            elif kind == 'BRACKETS':
                back.append(Brackets(value, self))

        return back

    @staticmethod
    def solve(formula: list) -> float:

        while any(True for t in formula if isinstance(t, Operator) and t.type in '*/%'):
            try:
                i = next(i for i, t in enumerate(formula) if isinstance(t, Operator)
                         and t.type in '*/%' and 0 < i < len(formula))
            except StopIteration:
                break
            formula[i] = Number(formula[i].do(formula[i - 1].val, formula[i + 1].val))
            del formula[i + 1]
            del formula[i - 1]

        while any(True for t in formula if isinstance(t, Operator)):
            try:
                i = next(i for i, t in enumerate(formula) if isinstance(t, Operator) and 0 < i < len(formula))
            except StopIteration:
                break
            formula[i] = Number(formula[i].do(formula[i - 1].val, formula[i + 1].val))
            del formula[i + 1]
            del formula[i - 1]

        if len(formula) == 2 and isinstance(formula[0], Operator) and formula[0].type in '+-':
            return formula[0].do(0, 1) * formula[1].val
        elif len(formula) != 1:
            print(formula)
            raise MathError()

        return formula[0].val


class Printable:
    val: float

    def __repr__(self):
        return "{}({})".format(self.__class__.__qualname__, getattr(self, 'val', getattr(self, 'type', None)))


class Number(Printable):
    def __init__(self, val: str):
        try:
            self.val = float(val)  # parse float (ex 14.9)
        except ValueError:
            try:
                self.val = float(int(val))  # parse int (to float) (ex 8)
            except ValueError:
                raise NumberParseError("can't parse {!r}".format(val))


class Variable(Printable):
    def __init__(self, val: str, compiler: MathCompiler):
        self.compiler = compiler
        try:
            self.name = val
            try:
                self.val = self.compiler.constants[val]
            except KeyError:
                self.val = self.compiler.variables[val]
        except KeyError:
            raise VariableMissingError("can't find {!r}".format(val))


class Operator(Printable):
    def __init__(self, key: str):
        self.type = key
        self.do = operator_index[key]


class Snipped(Printable):
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
