node a {}

walker init {
    root {
        take --> node::a;
    }

    a {
        report here;
    }
}