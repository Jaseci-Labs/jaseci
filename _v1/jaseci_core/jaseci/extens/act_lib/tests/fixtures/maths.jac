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

walker gcd_test{
    can maths.gcd;
    _list = [1,2,34,5,6];

    report maths.gcd(_list);
}

walker isclose_test{
    can maths.isclose;
    a = 23;
    b = 24;

    report maths.isclose(a,b);
}

walker isfinite_test{
    can maths.isfinite;
    a = 0.0;

    report maths.isfinite(a);
}

walker isinf_test{
    can maths.isinf;
    a = 0.0;

    report maths.isinf(a);
}

walker isnan_test{
    can maths.isnan;
    a = 0.0;

    report maths.isnan(a);
}

walker isqrt_test{
    can maths.isqrt;
    x = 9;

    report maths.isqrt(x);
}

walker lcm_test{
    can maths.lcm;
    _list = [1,2,3,4,5,7];

    report maths.lcm(_list);
}

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

walker prod_test{
    can maths.prod;
    _list = [2,3,4,5];

    report maths.prod(_list);
}

walker remainder_test{
    can maths.remainder;
    x = 23;
    y = 3;

    report maths.remainder(y,x);
}

walker trunc_test{
    can maths.trunc;
    x = 23.09;

    report maths.trunc(x);
}

walker ulp_test{
    can maths.ulp;
    x = 23.09;

    report maths.ulp(x);
}

walker cubert_test{
    can maths.cubert;
    x = 27;

    report maths.cubert(x);
}

walker exp_test{
    can maths.exp;
    x = 27;

    report maths.exp(x);
}

walker log_test{
    can maths.log;
    value = 27;
    base = 10;

    report maths.log(value,base);
}


