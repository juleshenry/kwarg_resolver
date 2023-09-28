# K-Warg Swiss Army Knife

The kwarg_solver decorator works in the following way:

If a decorator is placed over an empty stub function, and a method is implemented

this decorator finds the correct internal method 'decorated_method__X' and calls it with 

all but one argument not present in the original.



Example : 

```
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

```