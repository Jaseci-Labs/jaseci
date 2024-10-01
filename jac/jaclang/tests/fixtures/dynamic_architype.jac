import:py from jaclang.runtimelib.machine {JacMachine}

walker test_walker {
    can visit_nodes with `root entry {
        visit [-->](`?test_node);
    }
}

walker child_walker :test_walker: {}

node test_node {
    has value:int;

    can print_value with test_walker entry {
        print("Value:", f'{self.value}');
    }
}

with entry {
    for value in range(1, 4) {
        root ++> test_node(value=value);
    }
    node_obj = JacMachine.get().spawn_node('test_node', {'value': 0});
    walker_obj = JacMachine.get().spawn_walker('child_walker');
    root spawn walker_obj;
}
