node Node {
    has val: str;

    can entry1 with entry {
        print(f"{self.val}-4");
    }

    ######################################################
    #      NOT SUPPORTED YET IF IT'S DECLARED FIRST      #
    ######################################################
    #
    # can entry2 with "Walker" entry {
    #     print(5);
    # }
    #
    # can exit1 with "Walker" exit {
    #     print(6);
    # }
    #
    ######################################################
    # -------------------------------------------------- #
    ######################################################


    can exit2 with exit {
        print(f"{self.val}-7");
    }
}
walker Walker {
    can entry1 with entry {
        print(1);
    }

    can entry2 with `root entry {
        print(2);
        visit [-->];
    }

    can entry3 with Node entry {
        print(f"{here.val}-3");
    }

    can exit1 with Node exit {
        print(f"{here.val}-8");
    }

    can exit2 with exit {
        print(9);
    }
}
with entry{
    root ++> Node(val = "a");
    root ++> Node(val = "b");
    root ++> Node(val = "c");

    Walker() spawn root;
}