node tester {
    can testing {
        report std;
        std.set_global = 1;
        report std;
        std = 1;
        report std;
    }
}

walker check {

    with entry {
        take --> node::tester else {
            take spawn here ++> node::tester;
        }
    }

    tester {
        here::testing;
        report std;
    }
}