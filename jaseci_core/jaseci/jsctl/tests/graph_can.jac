graph rando {
    has anchor rt;
    can infer.year_from_date;
    spawn {
        rt=spawn node::generic;
        std.out(infer.year_from_date("2020-07-10"));
    }
}

walker go {
    spawn here --> graph::rando;
}