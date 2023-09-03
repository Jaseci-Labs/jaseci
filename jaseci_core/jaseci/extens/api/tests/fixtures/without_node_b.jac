node a {}

walker init {
    root {
        take -->;
        spawn --> walker::sample;
    }

    a {
        report here.info.name;
    }
}

walker sample {
    with entry {
        report here.info.name;
    }
}