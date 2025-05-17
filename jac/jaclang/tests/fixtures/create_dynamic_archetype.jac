import from jaclang.runtimelib.machine { JacMachineInterface, JacMachine }
# Dynamically create a node archetype
glob source_code = """
node dynamic_node {
has value:int;
can print_value with entry {
print("Dynamic Node Value:", f'{self.value}');
}
}
""";

# Create a new walker archetype dynamically
glob walker_code = """
walker dynamic_walker {
can visit_nodes with entry {
visit [-->];
}
}
""";

with entry {
    node_arch = JacMachineInterface.create_archetype_from_source(JacMachineInterface.py_get_jac_machine(), source_code);
    walker_arch = JacMachineInterface.create_archetype_from_source(JacMachineInterface.py_get_jac_machine(), walker_code);

    node_obj = JacMachineInterface.spawn_node(JacMachineInterface.py_get_jac_machine(),
        'dynamic_node',
        {'value': 99},
        node_arch.__name__
    );
    walker_obj = JacMachineInterface.spawn_walker(JacMachineInterface.py_get_jac_machine(),
        'dynamic_walker',
        module_name=walker_arch.__name__
    );
    node_obj spawn walker_obj;
}
