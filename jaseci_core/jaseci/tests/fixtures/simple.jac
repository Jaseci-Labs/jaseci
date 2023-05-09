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

walker complex {
    for i = 0 to i < 1000 by i+=1 {
        spawn here walker::creater;
    }
}

walker creater {
    root {
        new_node = spawn here ++> node::simple;
    }
}
