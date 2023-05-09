node simple {has a=4,b=5,c=3;}

walker init {
    root {
        new_node = spawn here ++> node::simple;
        report new_node;
    }
}

walker deep_except {
    report "Before try block";
    try {
        invalid_id = "xxxx.xxxx";
        report *(invalid_id);
        report "After trying to reference an invalid object id.";
    } else with error {
        report "Exception caught";
        report error;
    }
}

node cnode {
    has a=4,b=5,c=3;
    can jump with complex entry {
        a=b+c;
        b=a+c;
        c=a+b;
    }
}

walker complex {
    has limit = 130;
    root {
            spawn here walker::creater;
    }
    cnode {
        a = spawn here ++> node::cnode;
        spawn a walker::other;
    }
    if limit {take -->; limit-=1;}
}

walker other{
    take <--;
}

walker creater {
    root {
        new_node = spawn here ++> node::cnode;
    }
}
