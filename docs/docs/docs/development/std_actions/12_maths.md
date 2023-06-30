# Maths Actions Library

Math standard action library enables mathematical functions in Jaseci and provide following actions, all of which yield float values unless explicitly specified otherwise.

## Ceil

Return the ceiling of x, the smallest integer greater than or equal to x. If x is not a float, delegates to

Jac Example:

```jac
walker search{
    can math.ceil;
    _float = 123.45;

    report math.search(_float);
}
```

## Comb

Return the number of ways to choose k items from n items without repetition and without order.

Jac Example:

```jac
walker search{
    can math.comb;
}
```

## Copysign

Return a float with the magnitude (absolute value) of x but the sign of y.

Jac Example:

```jac
walker search{
    can math.copysign;
}
```

## Fabs

Return the absolute value of x.

## Factorial

Return n factorial as an integer.

## Floor

Return the floor of x, the largest integer less than or equal to x.

## Fmod

## Frexp

Return the mantissa and exponent of x as the pair (m, e).

## Fsum

Return an accurate floating point sum of values in the iterable.

## Gcd

Return the greatest common divisor of the specified integer arguments.

## isclose

Return True if the values a and b are close to each other and False otherwise.

## isfinite

Return True if x is neither an infinity nor a NaN, and False otherwise.

## isinf

Return True if x is a positive or negative infinity, and False otherwise.

## isnan

Return True if x is a NaN (not a number), and False otherwise.

## isqrt

Return the integer square root of the nonnegative integer n. This is the floor of the exact square root of n, or equivalently the greatest integer a such that a² ≤ n.

## lcm

Return the least common multiple of the specified integer arguments.

## ldexp

Return x * (2**i).

## modf

Return the fractional and integer parts of x. Both results carry the sign of x and are floats.

## nextafter

Return the next floating-point value after x towards y.

## perm

Return the number of ways to choose k items from n items without repetition and with order.

## Prod

Calculate the product of all the elements in the input iterable.

## remainder

Calculate the remainder

## trunc

Return x with the fractional part removed, leaving the integer part.

## ulp

Return the value of the least significant bit of the float x:

