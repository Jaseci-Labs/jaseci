walker ceil_test{
    can maths.ceil;
    _float = 123.45;

    report maths.ceil(_float);
}
walker comb_test{
    can maths.comb;
    n = 100;
    k = 2;

    report maths.comb(n,k);
}

walker copysign_test{
    can maths.copysign;
    x = 100;
    y = -2;

    report maths.copysign(x,y);
}

walker fabs_test{
    can maths.fabs;
    x = 10;

    report maths.fabs(x);
}

walker factorial_test{
    can maths.factorial;
    x = 10;

    report maths.factorial(x);
}

walker floor_test{
    can maths.floor;
    _float = 10.5;

    report maths.floor(_float);
}

walker fmod_test{
    can maths.fmod;
    x = 100;
    y = 3;

    report maths.fmod(x,y);
}

walker frexp_test{
    can maths.frexp;
    x = 100;

    report maths.frexp(x);
}

walker fsum_test{
    can maths.fsum;
    x = [1,2,4,5,6];

    report maths.fsum(x);
}

## gcd todo

## isclose todo

## isfinite todo

## isinf todo

## isnan toto

walker isqrt_test{
    can maths.isqrt;
    x = 9;

    report maths.isqrt(x);
}

## lcm todo

walker ldexp_test{
    can maths.ldexp;
    x = 9;
    i = 2;

    report maths.ldexp(x,i);
}

walker modf_test{
    can maths.modf;
    x = 9;

    report maths.modf(x);
}

walker nextafter_test{
    can maths.nextafter;
    x = 9;
    y = 3;

    report maths.nextafter(x,y);
}

walker perm_test{
    can maths.perm;
    x = 23;

    report maths.perm(x);
}

## prod todo



