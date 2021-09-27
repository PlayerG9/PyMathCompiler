class MathCompiler:
    def compute(self, equation: str, variables: dict) -> float:
        pass


default_compiler = MathCompiler()


def compute(equation: str, **kwargs):
    default_compiler.compute(equation, kwargs)
