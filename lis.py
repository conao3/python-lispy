from __future__ import annotations

import math
import operator
from collections.abc import Callable
from typing import Any
from typing import Self

################ Lispy: Scheme Interpreter in Python
## (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html


################ Utils


def trap[T](fn: Callable[[], T]) -> tuple[T, None] | tuple[None, Exception]:
    "Run fn, return (result, None) unless exception, then (None, exception)."
    try:
        return (fn(), None)

    except Exception as e:
        return (None, e)


################ Types


class Symbol(str):
    "A Lisp Symbol is implemented as a Python str"


type Value = int | float | Symbol | list[Value] | Callable[..., Value] | Procedure


################ Parsing: parse, tokenize, and read_from_tokens


def parse(program: str) -> Value:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))


def tokenize(s: str) -> list[str]:
    "Convert a string into a list of tokens."
    return s.replace("(", " ( ").replace(")", " ) ").split()


def read_from_tokens(tokens: list[str]) -> Value:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF while reading")

    token = tokens.pop(0)

    if "(" == token:
        lst: list[Value] = []

        while tokens[0] != ")":
            lst.append(read_from_tokens(tokens))

        tokens.pop(0)  # pop off ')'

        return lst

    elif ")" == token:
        raise SyntaxError("unexpected )")

    else:
        return atom(token)


def atom(token: str) -> Any:
    "Numbers become numbers; every other token is a symbol."
    ret, err = trap(lambda: int(token))
    if err is None:
        return ret

    ret, err = trap(lambda: float(token))
    if err is None:
        return ret

    return Symbol(token)


################ Environments


def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update(
        {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "=": operator.eq,
            "abs": abs,
            "append": operator.add,
            # "apply": apply,
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "eq?": operator.is_,
            "equal?": operator.eq,
            "length": len,
            "list": lambda *x: list(x),
            "list?": lambda x: isinstance(x, list),
            "map": map,
            "max": max,
            "min": min,
            "not": operator.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, int, float),
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
        },
    )
    return env


class Env(dict[str, Any]):
    "An environment: a dict of {'var':val} pairs, with an outer Env."

    def __init__(
        self,
        parms: tuple[str, ...] = (),
        args: tuple[Value, ...] = (),
        outer: Env | None = None,
    ):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var: str) -> Self:
        "Find the innermost Env where var appears."
        if var in self:
            return self

        if self.outer is None:
            raise KeyError(var)

        return self.outer.find(var)


global_env = standard_env()


################ Interaction: A REPL


def repl(prompt: str = "lis.py> "):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(input(prompt)))
        print(lispstr(val))


def lispstr(exp: Value) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return "(" + " ".join(map(lispstr, exp)) + ")"

    return str(exp)


################ Procedures


class Procedure:
    "A user-defined Scheme procedure."

    def __init__(self, parms: Any, body: Any, env: Env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args: Value) -> Value:
        return eval(self.body, Env(self.parms, args, self.env))


################ eval


def eval(x: Value, env: Env = global_env) -> Value:
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):  # variable reference
        return env.find(x)[x]

    elif not isinstance(x, list):  # constant literal
        return x

    elif x[0] == "quote":  # (quote exp)
        (_, exp) = x
        return exp

    elif x[0] == "if":  # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)

    elif x[0] == "define":  # (define var exp)
        (_, var, exp) = x
        assert isinstance(var, Symbol), "can only define symbols"
        env[var] = eval(exp, env)

    elif x[0] == "set!":  # (set! var exp)
        (_, var, exp) = x
        assert isinstance(var, Symbol), "can only set! symbols"
        env.find(var)[var] = eval(exp, env)

    elif x[0] == "lambda":  # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)

    proc = eval(x[0], env)
    assert callable(proc), f"{x[0]} is not callable"

    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)


if __name__ == "__main__":
    repl()
