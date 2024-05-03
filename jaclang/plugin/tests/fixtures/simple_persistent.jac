node a {
    has name:str;
}

node b {
    has name:str;
}

walker create {
    can setup with `root entry {
        print("in create setup");
        na = here ++> a(name="node a");
        visit na;
    }

    can ata with a entry {
        print("in create ata");
        here ++> b(name="node b");
    }

}


walker traverse {
    can at_root with `root entry {
        visit [-->];
    }

    can at_a with a entry {
        print(here);
        visit [-->];
    }

    can at_b with b entry {
        print(here);
    }
}

with entry {
    root spawn create();
}