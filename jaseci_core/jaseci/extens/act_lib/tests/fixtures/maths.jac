walker ceil_test{
    can math.ceil;
    _string = "set width=20 and height=10";

    report regex.findall("(\\w+)=(\\d+)", _string);
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