# Maths Actions Library

Math standard action library enables mathematical functions in Jaseci and provide following actions, all of which yield float values unless explicitly specified otherwise.

## Ceil

Return the ceiling of x, the smallest integer greater than or equal to x. If x is not a float, delegates to

Jac Example:

```jac
walker init{
    can maths.ceil;
    _float = 123.45;

    report maths.ceil(_float);
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

Jac Program:
```jac
walker init{
    can maths.floor;
    _float = 10.5;

    report maths.floor(_float);
}
```
Expected output:

```json
{
  "success": true,
  "report": [
    10
  ],
  "final_node": "urn:uuid:558001f2-7a27-4799-be46-6aa93e23cd79",
  "yielded": false
}
```

## Fmod

Expected Output:

Example Jac:

```jac
walker init{
    can maths.fmod;
    x = 100;
    y = 3;

    report maths.fmod(x,y);
}
```

```json
{
  "success": true,
  "report": [
    1.0
  ],
  "final_node": "urn:uuid:0ac023fb-a855-4784-bb1b-9596a450bc38",
  "yielded": false
}
```

## Frexp

Return the mantissa and exponent of x as the pair (m, e).

Example Jac:

```jac
walker init{
    can maths.frexp;
    x = 100;

    report maths.frexp(x);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    [
      0.78125,
      7
    ]
  ],
  "final_node": "urn:uuid:0be8e1a4-6961-4f63-a1c1-dd5ece2db5d2",
  "yielded": false
}
```

## Fsum

Return an accurate floating point sum of values in the iterable.

Example Jac:

```jac
walker init{
    can maths.fsum;
    x = [1,2,4,5,6];

    report maths.fsum(x);
}

```

Expected Output:

```json
{
  "success": true,
  "report": [
    18.0
  ],
  "final_node": "urn:uuid:780cdac0-b704-4233-ae2d-516f055e6f55",
  "yielded": false
}
```

## isqrt

Return the integer square root of the nonnegative integer n. This is the floor of the exact square root of n, or equivalently the greatest integer a such that a² ≤ n.

Example Jac:

```jac
walker init{
    can maths.isqrt;
    x = 9;

    report maths.isqrt(x);
}

```

Expected Output:

```json
{
  "success": true,
  "report": [
    3
  ],
  "final_node": "urn:uuid:35170582-7023-4686-ae08-222a54d0e92a",
  "yielded": false
}
```

## ldexp

Return x * (2**i).

Example Jac:

```jac
walker init{
    can maths.ldexp;
    x = 9;
    i = 2;

    report maths.ldexp(x,i);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    36.0
  ],
  "final_node": "urn:uuid:462546a4-4534-4101-8f61-78d9ee4cf8a5",
  "yielded": false
}
```

## modf

Return the fractional and integer parts of x. Both results carry the sign of x and are floats.

Example Jac:

```jac
walker init{
    can maths.modf;
    x = 9;

    report maths.modf(x);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    [
      0.0,
      9.0
    ]
  ],
  "final_node": "urn:uuid:eb4e1dfa-0972-4cbe-804e-1a682f4b4572",
  "yielded": false
}
```

## nextafter

Return the next floating-point value after x towards y.

Example Jac:

```jac
walker init{
    can maths.nextafter;
    x = 9;
    y = 3;

    report maths.nextafter(x,y);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    8.999999999999998
  ],
  "final_node": "urn:uuid:f4080344-882b-4c56-aa6f-f20ec8fd3469",
  "yielded": false
}
```

## perm

Return the number of ways to choose k items from n items without repetition and with order.

Example Jac:

```jac
walker init{
    can maths.perm;
    x = 23;

    report maths.perm(x);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    25852016738884976640000
  ],
  "final_node": "urn:uuid:ebf16935-cd09-40d4-b956-abf43a62a215",
  "yielded": false
}
```