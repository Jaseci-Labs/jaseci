


node person{
    has age:int;
}

with entry{
    p1 = person(10);
    p2 = person(20);
    p3 = person(30);
    p4  = person(40);


    root ++> p1;
    p1 ++> p2;
    p2 ++> p3;
    p3 ++> p4;


    del p2;
    

}