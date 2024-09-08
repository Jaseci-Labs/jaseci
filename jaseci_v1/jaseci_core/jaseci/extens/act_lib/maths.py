import math

from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action()
def ceil(x):
    # return int
    return math.ceil(x)


@jaseci_action()
def comb(n, k):
    # return int
    return math.comb(n, k)


@jaseci_action()
def copysign(x, y):
    # return float
    return math.copysign(x, y)


@jaseci_action()
def fabs(x):
    # return float
    return math.fabs(x)


@jaseci_action()
def factorial(n):
    # return int
    return math.factorial(n)


@jaseci_action()
def floor(x):
    # return int
    return math.floor(x)


@jaseci_action()
def fmod(x, y):
    # return float
    return math.fmod(x, y)


@jaseci_action()
def frexp(x):
    # return tuple
    _tuple = math.frexp(x)
    return list(_tuple)


@jaseci_action()
def fsum(iterable: list):
    # return float
    return math.fsum(iterable)


@jaseci_action()
def gcd(args: list):
    args = tuple(args)
    # return int
    return math.gcd(*args)


@jaseci_action()
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    # return boolean
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


@jaseci_action()
def isfinite(x):
    # return boolean
    return math.isfinite(x)


@jaseci_action()
def isinf(x):
    # return boolean
    return math.isinf(x)


@jaseci_action()
def isnan(x):
    # return boolean
    return math.isnan(x)


@jaseci_action()
def isqrt(n):
    # return int
    return math.isqrt(n)


@jaseci_action()
def lcm(args: list):
    args = tuple(args)
    # return int
    return math.lcm(*args)


@jaseci_action()
def ldexp(x, i):
    # return float
    return math.ldexp(x, i)


@jaseci_action()
def modf(x):
    _tupple = math.modf(x)
    # return list
    return list(_tupple)


@jaseci_action()
def nextafter(x, y):
    # return float
    return math.nextafter(x, y)


@jaseci_action()
def perm(n, k=None):
    # return int
    return math.perm(n, k)


@jaseci_action()
def prod(iterable, start=1):
    return math.prod(iterable, start=start)


@jaseci_action()
def remainder(x, y):
    # return float
    return math.remainder(x, y)


@jaseci_action()
def trunc(x):
    # return int
    return math.trunc(x)


@jaseci_action()
def ulp(x):
    # return float
    return math.ulp(x)


@jaseci_action()
def cubert(x):
    # return float
    return x ** (1 / 3)


@jaseci_action()
def exp(x):
    # return float
    return math.exp(x)


@jaseci_action()
def log(x, base):
    # return float
    return math.log(x, base)
