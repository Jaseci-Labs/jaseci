node a {
    has val;
}

walker init {
    root: take --> node::a else: take spawn here ++> node::a;
    a: report here;
}

walker scheduled_walker {
    root: take --> node::a;
    a: report here.val = true;
}

walker scheduled_sequence {
    root: take --> node::a;
    a: report here.val = false;
}