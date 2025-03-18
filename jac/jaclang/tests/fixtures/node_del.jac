


node person{
    has age:int;
}

with entry{
    p1 = person(10);
    p2 = person(20);
    p3 = person(30);
    p4 = person(40);
    p5 = person(50);


    root ++> p1;
    root ++> p2;

    p1 ++> p3;
    p2 ++> p3;

    p3 ++> p4;
    p3 ++> p5;

    del p3;

}