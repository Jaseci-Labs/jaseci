node simple {has a=4,b=5,c=3;}

walker most_basic {
    report 4 + 5000;
    var="b";

    report 6-2-3;
    report "a"+var;
    x={"base": 5};
    x["test"]=5;
    report x;

    a = spawn node::simple;
    b = spawn node::simple(a=3,b=55,c=311);
    a := b;
    report a.context;
}

