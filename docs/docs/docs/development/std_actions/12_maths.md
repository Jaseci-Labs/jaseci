# Maths Actions Library

Math standard action library enables mathematical functions in Jaseci and provide following actions, all of which yield float values unless explicitly specified otherwise.

## Ceil

Return the ceiling of x, the smallest integer greater than or equal to x. If x is not a float, delegates to

Jac Example:

```jac
walker init{
    can math.ceil;
    _float = 123.45;

    report math.search(_float);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    124
  ],
  "final_node": "urn:uuid:41800be0-01b4-4658-b49d-48b3623d40cf",
  "yielded": false
}
```

## Comb

Return the number of ways to choose k items from n items without repetition and without order.

Jac Example:

```jac
walker init{
    can maths.comb;
    n = 100;
    k = 2;

    report maths.comb(n,k);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    4950
  ],
  "final_node": "urn:uuid:0d970260-4e00-475e-a9ef-58dcf159e670",
  "yielded": false
}
```

## Copysign

Return a float with the magnitude (absolute value) of x but the sign of y.

Jac Example:

```jac
walker init{
    can maths.copysign;
    x = 100;
    y = -2;

    report maths.copysign(x,y);
}
```

Expected Output:

```
{
  "success": true,
  "report": [
    -100.0
  ],
  "final_node": "urn:uuid:b170034a-d289-4b4a-b300-3575430e238e",
  "yielded": false
}
```

## Fabs

Return the absolute value of x.

Jac Example:

```jac
walker init{
    can maths.fabs;
    x = 10;

    report maths.fabs(x);
}
```

Expected Output
```json
{
  "success": true,
  "report": [
    10.0
  ],
  "final_node": "urn:uuid:d72a7dac-b9ad-4589-8829-fa1cad9fa732",
  "yielded": false
}
```

## Factorial

Return n factorial as an integer.

Jac Program:

```jac
walker init{
    can maths.factorial;
    x = 10;

    report maths.factorial(x);
}
```

Expected Output:
```json
{
  "success": true,
  "report": [
    3628800
  ],
  "final_node": "urn:uuid:08f1c327-3b35-411e-b132-0ec24256c948",
  "yielded": false
}
```

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

