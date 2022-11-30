node simple {has a=4,b=5,c=3;}

walker init {
    root {
        new_node = spawn here ++> node::simple;
        report new_node;
    }
}

walker deep_except {
    std.log("Before try block");
    try {
        invalid_id = "xxxx.xxxx";
        std.log(*(invalid_id));
        std.log("After trying to reference an invalid object id.");
    } else with error {
        std.log("Exception caught");
        std.log(error);
    }
}