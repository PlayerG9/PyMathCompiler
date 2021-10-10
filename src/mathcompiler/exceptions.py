class MathError(Exception): pass
class NumberParseError(MathError): pass
class VariableMissingError(MathError): pass
class FunctionMissingError(MathError): pass
class MissingBracketError(MathError): pass
