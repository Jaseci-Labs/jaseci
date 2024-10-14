node test_node {
    has value: int;
}

walker test_walker {
    has visited_nodes: list = [];
    has entry_count: int = 0;
    has exit_count: int = 0;

    can walker_entry with entry {
        print("Walker entry: ",here);
        self.entry_count += 1;
    }

    can node_entry with `root entry {
        visit [-->](`?test_node);
        print("Node entry: ",here);
    }

    can node_exit with test_node exit {
        print("Node exit: ", here);
        self.visited_nodes.append(here);
    }

    can walker_exit with exit {
        print("Walker exit: ",here);
        self.exit_count += 1;
    }
}

with entry {
    for i in range(5) {
        root ++> (next:=test_node(value=i));
    }
    visitor = root spawn test_walker();
    print(visitor.visited_nodes);
}
