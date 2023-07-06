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
## GCD

Return the greatest common divisor of the specified integer arguments.

Example Jac:

```jac
walker init{
    can maths.gcd;
    _list = [1,2,34,5,6];

    report maths.gcd(_list);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    1
  ],
  "final_node": "urn:uuid:611f0fd1-6506-4178-a8c9-7d47570ca12b",
  "yielded": false
}
```

## isclose

Return True if the values a and b are close to each other and False otherwise.

Example Jac:

```jac
walker init{
    can maths.isclose;
    a = 23;
    b = 24;

    report maths.isclose(a,b);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    false
  ],
  "final_node": "urn:uuid:3d8f257a-a82c-4da5-b262-60422100cccb",
  "yielded": false
}
```

## isfinite

Return True if x is neither an infinity nor a NaN, and False otherwise.

Example Jac:

```jac
walker init{
    can maths.isfinite;
    a = 0.0;

    report maths.isfinite(a);
}
```

Example Output:
```json
{
  "success": true,
  "report": [
    true
  ],
  "final_node": "urn:uuid:399e10ae-bdfd-4590-be51-9e0ee935247c",
  "yielded": false
}
```

## isinf

Return True if x is a positive or negative infinity, and False otherwise.

Example Jac:

```jac
walker init{
    can maths.isinf;
    a = 0.0;

    report maths.isinf(a);
}
```

```json
{
  "success": true,
  "report": [
    false
  ],
  "final_node": "urn:uuid:5587a028-5487-4fcd-a701-b33c024e976e",
  "yielded": false
}
```

## isnan

Return True if x is a NaN (not a number), and False otherwise.

Example Jac:

```jac
walker init{
    can maths.isnan;
    a = 0.0;

    report maths.isnan(a);
}
```

```json
{
  "success": true,
  "report": [
    false
  ],
  "final_node": "urn:uuid:2aa812ad-2dc2-44c7-95b9-527efc7236c4",
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

## lcm

Return the least common multiple of the specified integer arguments.

Example Jac:

```jac
walker init{
    can maths.lcm;
    _list = [1,2,3,4,5,7];

    report maths.lcm(_list);
}
```

```json
{
  "success": true,
  "report": [
    420
  ],
  "final_node": "urn:uuid:81e962fd-86c3-4ebe-8b3d-8410149a542a",
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

## Prod

Calculate the product of all the elements in the input iterable.

Example Jac:

```jac
walker init{
    can maths.prod;
    _list = [2,3,4,5];

    report maths.prod(_list);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    120
  ],
  "final_node": "urn:uuid:140fbcc6-e845-4655-be46-0cb883f00d0c",
  "yielded": false
}
```

## remainder

Calculate the remainder

Example Jac:

```jac
walker init{
    can maths.remainder;
    x = 23;
    y = 3;

    report maths.remainder(y,x);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    3.0
  ],
  "final_node": "urn:uuid:f23a45ca-d0a2-4b26-93dd-69d2662756cf",
  "yielded": false
}
```

## trunc

Return x with the fractional part removed, leaving the integer part.

Example Jac:

```jac
walker init{
    can maths.trunc;
    x = 23.09;

    report maths.trunc(x);
}
```

Expected Output:

```json
{
  "success": true,
  "report": [
    23
  ],
  "final_node": "urn:uuid:edf78eec-b246-4d06-923c-6e3c52944884",
  "yielded": false
}
```

## ulp

Return the value of the least significant bit of the float x:

Example Jac:

```jac
walker init{
    can maths.ulp;
    x = 23.09;

    report maths.ulp(x);
}
```

Expected Jac:
```json
{
  "success": true,
  "report": [
    3.552713678800501e-15
  ],
  "final_node": "urn:uuid:34690881-4e35-4c6e-8368-073b34709b96",
  "yielded": false
}
```

## cubert

Return the cube root of x.

Example Jac:
```jac
walker init{
    can maths.cubert;
    x = 27;

    report maths.cubert(x);
}
```

Expected Output:
```json
{
  "success": true,
  "report": [
    3.0
  ],
  "final_node": "urn:uuid:d29addf8-3867-4bd3-8860-304335f261a1",
  "yielded": false
}
```

## exp

Return e raised to the power x, where e = 2.718281… is the base of natural logarithms. This is usually more accurate than math.e ** x or pow(math.e, x).

Example Jac:
```jac
walker init{
    can maths.exp;
    x = 27;

    report maths.exp(x);
}
```

Expected Output:
```json
{
  "success": true,
  "report": [
    532048240601.79865
  ],
  "final_node": "urn:uuid:961e2e5b-97e3-4b4c-b1c9-e441d58e1207",
  "yielded": false
}
```

## log

With one argument, return the natural logarithm of x (to base e).

Example Jac:

```jac
walker init{
    can maths.log;
    value = 27;
    base = 10;

    report maths.log(value,base);
}
```

```json
{
  "success": true,
  "report": [
    1.4313637641589871
  ],
  "final_node": "urn:uuid:ecef5737-69d4-432c-bc96-726e3a5418d2",
  "yielded": false
}
```