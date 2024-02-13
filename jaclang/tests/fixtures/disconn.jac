node c{
    has cc : int=9;
}
edge aaa{
        has vvv:int=45;
}


node a{
    has aa:int =1;
}
node b{
    has bb:int =4;
}
with entry{
    x=[a(aa=x) for x in range(0,3)];
    y=[b(bb=x) for x in range(0,3)];
    z=[c(cc=x) for x in range(0,3)];
    x++>y;
    y++>z;

    # print(x -:aaa:-> );
    # print(x[1]._jac_.edges);  #uncomment line 23 and 28 to confirm
                                # the created edges while connecting are destroyed while disconnect
    print(x --> y-->z);
    print(x-->);
    print(x del--> y);
    print(x -->);
    # print(x[1]._jac_.edges);
    # print(x[1]._jac_.gen_dot());

    # print(x[1]-->z,'it should be [bb=0 bb=1 bb=2]');

}