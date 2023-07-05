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


# todo gcd,isclose,isfinite,isinf,isnan


@jaseci_action()
def isqrt(n):
    # return int
    return math.isqrt(n)


# todo lcm


@jaseci_action()
def ldexp(x, i):
    # return float
    return math.ldexp(x, i)


@jaseci_action()
def modf(x):
    # return tupple
    _tupple = math.modf(x)
    return list(_tupple)


@jaseci_action()
def nextafter(x, y):
    # return float
    return math.nextafter(x, y)


@jaseci_action()
def perm(n, k=None):
    # return int
    return math.perm(n, k)


# todo prod


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


# todo power and logs
