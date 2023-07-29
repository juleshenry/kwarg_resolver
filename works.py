# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:56:16 CDT 2023

@author: Julian Henry

Allows for arbitrary missing variable resolution

Working examples. Wed May 24 22:19:54 CDT 2023
"""
import inspect
def kwarg_solver(func):
    """
    Intention:
    base method is `vanilla`... that means no `__syntax`

    and can calculate necessary formula to solve for a single variable

    Assumption: method is not static. why? we abuse inspect to inspect the
    [1:-1] kwargs in order to resolve the missing parameter
    """

    def wrapper(self, *args, **kwargs):
        method_name = func.__name__
        all_parameters = list(inspect.signature(func).parameters)[1:-1]
        missing_arg = [kw for kw in all_parameters if kw not in kwargs]
        if not len(missing_arg) == 1:
            raise ValueError(
                "Must have exactly one missing variable for which to solve."
            )
        correct_method = method_name + "__" + missing_arg[0]
        correct_args = [x[1] for x in sorted(kwargs.items(), key=lambda kv: kv[0])]
        return getattr(self, correct_method)(*correct_args)

    return wrapper


def einstein():
    class Einstein:
        @kwarg_solver
        def einstein(s, e: float = None, m: float = None, **kwargs):
            return  # decorator skips return

        def einstein__m(s, e: float):
            return e / 8.98755179e16

        def einstein__e(s, m: float) -> float:
            return m * 8.98755179e16


    e = Einstein()
    ans = e.einstein(e=1000)  # returns m, (1000 / 8.98755179 e16), ~1.11265 e -14
    assert 1.1126500557278013e-14 == (ans)
    ans = e.einstein(m=1000)  # returns e, 1000 * 8.98755179 e16, ~8.98755179 e19
    assert 8.98755179e+19 == (ans)
    ans = e.einstein(e=ans)  # returns e, 1000 * 8.98755179 e16, ~8.98755179 e19
    assert 1000.0 == (ans)


def pythagoras():
    class Pythagoras:
        @kwarg_solver
        def pythagorean(s, a: float = None, b: float = None, c: float = None, **kwargs):
            return

        def pythagorean__a(s, b: float, c: float):
            return (c ** 2 - b ** 2) ** 0.5

        def pythagorean__b(s, a: float, c: float):
            return (c ** 2 - a ** 2) ** 0.5

        def pythagorean__c(s, a: float, b: float):
            return (a ** 2 + b ** 2) ** 0.5


    p = Pythagoras()

    ans = p.pythagorean(a=12, c=13)  # 5
    assert 5 == (ans)
    ans = p.pythagorean(a=12, b=5)  # 12
    assert 12 == (ans)
    ans = p.pythagorean(b=12, c=13)  # 13
    assert 13 == (ans)


def vacuum_theory():
    class VacuumTheory:

        @kwarg_solver
        def eqn_1_3(s, k=None, m=None, T=None, **kwargs):
            return 

        def eqn_1_3__T(s, k: float, m: float):
            # .5 * m * v**2 = 1.5 * k * T
            result = []
            T = 0.333333333333333 * m  ** 2 / k
            result.append(T)
            return T

        def eqn_1_3__k(s, T: float, m: float):
            # .5 * m * v**2 = 1.5 * k * T
            result = []
            k = 0.333333333333333 * m  ** 2 / T
            result.append(k)
            return k

        def eqn_1_3__m(s, T: float, k: float):
            # .5 * m * v**2 = 1.5 * k * T
            result = []
            m = 3.0 * T * k ** 2
            result.append(m)
            return m

    VT = VacuumTheory()

    ans = VT.eqn_1_3(k=1, T=3)  # 5
    assert 5 == (ans)
    ans = VT.eqn_1_3(m=2, T=3)  # 12
    assert 12 == (ans)
    ans = VT.eqn_1_3(m=2, k=1)  # 13
    assert 13 == (ans)

if __name__=='__main__':
    einstein()
    pythagoras()
    vacuum_theory()
    print(✅)