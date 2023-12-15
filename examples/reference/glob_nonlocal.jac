glob x=5,y=10,z=1;

can foo() -> none {
    :g: x,y,z;
    y = 30;
    print(x,y);

    can foo2() ->int {
        :nl: y;
        y=9;
        return (x,y);
    }
    print(foo2());

}

with entry{
    print(foo());
}
