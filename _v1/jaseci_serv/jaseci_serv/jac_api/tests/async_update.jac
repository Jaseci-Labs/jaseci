node a {
    has value = false;
}
walker init {
    root {
        spawn here ++> node::a;
    }
}

async walker update_value {
    root {
        take --> node::a;
    }
    a {
        here.value = true;
        report here.context;
    }
}

walker get_value {
    root {
        take --> node::a;
    }
    a {
        report here.context;
    }
}