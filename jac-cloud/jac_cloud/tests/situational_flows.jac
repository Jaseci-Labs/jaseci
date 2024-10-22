#################################################################
#                    TESTING SPAWN WALKER                       #
#################################################################

node NodeTest {
    has value: int;
}

walker WalkerTestSpawn {
    has visited_nodes: list = [];
    has entry_count: int = 0;
    has exit_count: int = 0;

    can first_entry with entry{
        for i in range(5) {
            root ++> NodeTest(value=i);
        }
    }

    can walker_entry with entry {
        report f"Walker entry: {here}";
        self.entry_count += 1;
    }

    can node_entry with `root entry {
        visit [-->](`?NodeTest);
        report f"Node entry: {here}";
    }

    can node_exit with NodeTest exit {
        report f"Node exit: {here}";
        self.visited_nodes.append(here);
    }

    can walker_exit with exit {
        report f"Walker exit: {here}";
        self.exit_count += 1;

        report self;
    }

    class __specs__ {
        has auth: bool = False;
    }
}