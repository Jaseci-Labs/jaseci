node test_node {
    has value: int;
}

walker test_walker {
    has visited_nodes: list = [];
    has entry_count: int = 0;
    has exit_count: int = 0;

    can traverse with `root entry {
        visit [-->](`?test_node);
    }

    can log_entry with entry {
        self.entry_count += 1;
    }

    can log_exit with exit {
        self.exit_count += 1;
    }

    can log_visit with test_node exit {
        self.visited_nodes.append(here);
    }
}

with entry {
    for i in range(2) {
        root ++> (next:=test_node(value=i));
    }
    wlk_obj = root spawn test_walker();
    print(wlk_obj);
}