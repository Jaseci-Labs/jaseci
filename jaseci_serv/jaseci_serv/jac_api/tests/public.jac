node a {
    has value;
}

walker manual_init {
    root {
        a = spawn here ++> node::a(value="user");
        report a;
    }
}

walker show_a_details:requestor {
    a {
        report here;
        here.value = "changed";
        report here;
    }
}


walker callback:anyone {
    with entry {
        report:status = 200;
        report:custom = {
            "updated": false
        };
    }
}
