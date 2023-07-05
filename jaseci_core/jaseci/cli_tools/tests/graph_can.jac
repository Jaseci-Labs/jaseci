graph rando {
    has anchor rt;
    can infer.year_from_date;
    spawn {
        rt = spawn node::generic;
        std.out(infer.year_from_date("2020-07-10"));
    }
}

walker go1 {
    spawn here ++> graph::rando;
}

walker go2 {
    can infer.month_from_date;

    with entry {
        std.out(infer.month_from_date("2020-07-10"));
    }
}

node with_can {
    can infer.day_from_date, infer.month_from_date, infer.year_from_date;

    can check1 {
        std.out(infer.month_from_date("2020-07-10"));
    }

    can check2 with go3 entry {
        std.out(infer.year_from_date("2020-07-10"));
    }

    can check3 with go3 exit {
        std.out(infer.day_from_date("2020-07-10"));
    }
}

walker go3 {
    with entry {
        take --> node::with_can else {
            take spawn here ++> node::with_can;
        }
    }

    with_can {
        here::check1;
    }
}